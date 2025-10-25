<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';
import adminAuthService from '@/services/AdminAuthService';

const router = useRouter();
const questions = ref([]);
const isLoading = ref(false);
const token = ref('');

onMounted(async () => {
  token.value = adminAuthService.getToken();
  if (!token.value) {
    router.push('/admin/login');
    return;
  }
  await loadQuestions();
});

async function loadQuestions() {
  isLoading.value = true;
  try {
    const response = await quizApiService.getQuizInfo();
    if (response && response.data) {
      const questionsData = [];
      for (let i = 1; i <= response.data.size; i++) {
        try {
          const qResponse = await quizApiService.getQuestion(i, token.value);
          if (qResponse && qResponse.data) {
            questionsData.push(qResponse.data);
          }
        } catch (error) {
          console.error(`Erreur question ${i}:`, error);
        }
      }
      questions.value = questionsData;
    }
  } catch (error) {
    console.error('Erreur chargement questions:', error);
  } finally {
    isLoading.value = false;
  }
}

function createQuestion() {
  router.push('/admin/questions/create');
}

function editQuestion(questionId) {
  router.push(`/admin/questions/edit/${questionId}`);
}

async function deleteQuestion(questionId) {
  if (!confirm('Supprimer cette question ?')) {
    return;
  }

  try {
    await quizApiService.deleteQuestion(questionId, token.value);
    await loadQuestions();
    alert('Question supprimée');
  } catch (error) {
    console.error('Erreur suppression:', error);
    alert('Erreur lors de la suppression');
  }
}

async function deleteAllQuestions() {
  if (
    !confirm(
      'ATTENTION : Supprimer TOUTES les questions ? Action irréversible !'
    )
  ) {
    return;
  }

  try {
    await quizApiService.deleteAllQuestions(token.value);
    await loadQuestions();
    alert('Questions supprimées');
  } catch (error) {
    console.error('Erreur suppression:', error);
    alert('Erreur lors de la suppression');
  }
}

async function deleteAllParticipations() {
  if (
    !confirm(
      'Supprimer toutes les participations ?'
    )
  ) {
    return;
  }

  try {
    await quizApiService.deleteAllParticipations(token.value);
    alert('Participations supprimées');
  } catch (error) {
    console.error('Erreur suppression:', error);
    alert('Erreur lors de la suppression');
  }
}

async function rebuildDatabase() {
  if (
    !confirm(
      'ATTENTION : Reconstruire la BDD ? Toutes les données seront perdues !'
    )
  ) {
    return;
  }

  try {
    await quizApiService.rebuildDatabase(token.value);
    await loadQuestions();
    alert('BDD reconstruite');
  } catch (error) {
    console.error('Erreur reconstruction:', error);
    alert('Erreur lors de la reconstruction');
  }
}

function logout() {
  adminAuthService.clearToken();
  router.push('/admin/login');
}
</script>

<template>
  <div class="container mt-4">
    <div class="admin-header mb-4">
      <div class="d-flex justify-content-between align-items-center">
        <h1 class="h3 text-white mb-0">Gestion des Questions</h1>
        <button @click="logout" class="btn btn-outline-light">
          Déconnexion
        </button>
      </div>
    </div>

    <div class="row mb-4">
      <div class="col-md-12">
        <div class="btn-toolbar gap-2" role="toolbar">
          <button @click="createQuestion" class="btn btn-light">
            Créer une question
          </button>
          <button @click="deleteAllQuestions" class="btn btn-danger">
            Supprimer toutes les questions
          </button>
          <button @click="deleteAllParticipations" class="btn btn-warning">
            Supprimer toutes les participations
          </button>
          <button @click="rebuildDatabase" class="btn btn-secondary">
            Reconstruire la BDD
          </button>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-light" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
    </div>

    <div v-else class="card shadow-lg border-0">
      <div class="card-header bg-white border-0 py-4">
        <h2 class="h5 mb-0 text-dark">Liste des Questions</h2>
      </div>
      <div class="card-body p-0">
        <div v-if="questions.length === 0" class="text-center py-5">
          <p class="text-muted mb-3">Pas de questions</p>
          <button @click="createQuestion" class="btn btn-dark">
            Créer une question
          </button>
        </div>
        <div v-else class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th class="px-4 py-3">Position</th>
                <th class="px-4 py-3">ID</th>
                <th class="px-4 py-3">Titre</th>
                <th class="px-4 py-3 text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="q in questions" :key="q.id" class="question-row">
                <td class="px-4 py-3">
                  <span class="position-badge">{{ q.position }}</span>
                </td>
                <td class="px-4 py-3 text-muted">#{{ q.id }}</td>
                <td class="px-4 py-3 fw-semibold">{{ q.title }}</td>
                <td class="px-4 py-3 text-end">
                  <button
                    @click="editQuestion(q.id)"
                    class="btn btn-sm btn-outline-primary me-2"
                  >
                    Modifier
                  </button>
                  <button
                    @click="deleteQuestion(q.id)"
                    class="btn btn-sm btn-outline-danger"
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="mt-4 text-center">
      <router-link to="/" class="btn btn-outline-light">
        Retour à l'accueil
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.btn-toolbar {
  display: flex;
  flex-wrap: wrap;
}

.admin-header {
  background: rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 10px;
}

.card {
  border-radius: 15px;
}

.question-row {
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.question-row:hover {
  background-color: #f8f9fa;
  border-left-color: #667eea;
}

.position-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
}

.btn-light {
  background: white;
  border: none;
}

.btn-light:hover {
  background: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
