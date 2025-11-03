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
  <div>
    <div class="color-drops">
      <span v-for="n in 40" :key="n"></span>
    </div>
    <div class="container mt-4 mb-5 pb-5">
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
            <button @click="createQuestion" class="btn btn-gradient">
              Créer une question
            </button>
            <button @click="deleteAllQuestions" class="btn btn-danger-custom">
              Supprimer toutes les questions
            </button>
            <button @click="deleteAllParticipations" class="btn btn-warning-custom">
              Supprimer toutes les participations
            </button>
            <button @click="rebuildDatabase" class="btn btn-secondary-custom">
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

      <div v-else class="admin-container">
        <div class="admin-container-inner">
          <div class="admin-content-header py-4">
            <h2 class="h5 mb-0 text-white text-center">Liste des Questions</h2>
          </div>
          <div class="admin-content-body p-0">
            <div v-if="questions.length === 0" class="text-center py-5">
              <p class="text-white-50 mb-3">Pas de questions</p>
              <button @click="createQuestion" class="btn btn-gradient">
                Créer une question
              </button>
            </div>
            <div v-else class="table-responsive">
              <table class="table table-hover mb-0 table-custom">
                <thead class="table-header-custom">
                  <tr>
                    <th class="px-4 py-3 text-white">Position</th>
                    <th class="px-4 py-3 text-white">ID</th>
                    <th class="px-4 py-3 text-white">Titre</th>
                    <th class="px-4 py-3 text-end text-white">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="q in questions" :key="q.id" class="question-row">
                    <td class="px-4 py-3">
                      <span class="position-badge">{{ q.position }}</span>
                    </td>
                    <td class="px-4 py-3 text-white-50">#{{ q.id }}</td>
                    <td class="px-4 py-3 fw-semibold text-white">{{ q.title }}</td>
                    <td class="px-4 py-3 text-end">
                      <button
                        @click="editQuestion(q.id)"
                        class="btn btn-sm btn-outline-warning me-2"
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
      </div>

      <div class="mt-4 text-center">
        <router-link to="/" class="btn btn-outline-light">
          Retour à l'accueil
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.color-drops {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  z-index: -1;
  opacity: 0.4;
}

.color-drops span {
  position: absolute;
  top: -100%;
  width: 8px;
  height: 200px;
  background: linear-gradient(45deg, #f0bd1e, #cc13b5);
  border-radius: 50px;
  animation: drop linear infinite;
}

.color-drops span:nth-child(1) { left: 2%; animation-duration: 8s; animation-delay: 0s; }
.color-drops span:nth-child(2) { left: 5%; animation-duration: 12s; animation-delay: 1s; }
.color-drops span:nth-child(3) { left: 8%; animation-duration: 10s; animation-delay: 0.5s; }
.color-drops span:nth-child(4) { left: 12%; animation-duration: 14s; animation-delay: 2s; }
.color-drops span:nth-child(5) { left: 15%; animation-duration: 9s; animation-delay: 0.8s; }
.color-drops span:nth-child(6) { left: 18%; animation-duration: 11s; animation-delay: 1.5s; }
.color-drops span:nth-child(7) { left: 22%; animation-duration: 13s; animation-delay: 0.3s; }
.color-drops span:nth-child(8) { left: 25%; animation-duration: 7s; animation-delay: 1.8s; }
.color-drops span:nth-child(9) { left: 28%; animation-duration: 15s; animation-delay: 0.7s; }
.color-drops span:nth-child(10) { left: 32%; animation-duration: 8s; animation-delay: 2.2s; }
.color-drops span:nth-child(11) { left: 35%; animation-duration: 12s; animation-delay: 1.2s; }
.color-drops span:nth-child(12) { left: 38%; animation-duration: 10s; animation-delay: 0.9s; }
.color-drops span:nth-child(13) { left: 42%; animation-duration: 14s; animation-delay: 1.7s; }
.color-drops span:nth-child(14) { left: 45%; animation-duration: 9s; animation-delay: 0.4s; }
.color-drops span:nth-child(15) { left: 48%; animation-duration: 11s; animation-delay: 2.1s; }
.color-drops span:nth-child(16) { left: 52%; animation-duration: 13s; animation-delay: 0.6s; }
.color-drops span:nth-child(17) { left: 55%; animation-duration: 7s; animation-delay: 1.9s; }
.color-drops span:nth-child(18) { left: 58%; animation-duration: 15s; animation-delay: 1.1s; }
.color-drops span:nth-child(19) { left: 62%; animation-duration: 8s; animation-delay: 0.2s; }
.color-drops span:nth-child(20) { left: 65%; animation-duration: 12s; animation-delay: 1.6s; }
.color-drops span:nth-child(21) { left: 68%; animation-duration: 10s; animation-delay: 0.1s; }
.color-drops span:nth-child(22) { left: 72%; animation-duration: 14s; animation-delay: 2.3s; }
.color-drops span:nth-child(23) { left: 75%; animation-duration: 9s; animation-delay: 1.3s; }
.color-drops span:nth-child(24) { left: 78%; animation-duration: 11s; animation-delay: 0.5s; }
.color-drops span:nth-child(25) { left: 82%; animation-duration: 13s; animation-delay: 2s; }
.color-drops span:nth-child(26) { left: 85%; animation-duration: 7s; animation-delay: 0.8s; }
.color-drops span:nth-child(27) { left: 88%; animation-duration: 15s; animation-delay: 1.4s; }
.color-drops span:nth-child(28) { left: 92%; animation-duration: 8s; animation-delay: 0.7s; }
.color-drops span:nth-child(29) { left: 95%; animation-duration: 12s; animation-delay: 2.4s; }
.color-drops span:nth-child(30) { left: 98%; animation-duration: 10s; animation-delay: 1s; }
.color-drops span:nth-child(31) { left: 3%; animation-duration: 14s; animation-delay: 1.8s; }
.color-drops span:nth-child(32) { left: 7%; animation-duration: 9s; animation-delay: 0.3s; }
.color-drops span:nth-child(33) { left: 11%; animation-duration: 11s; animation-delay: 2.1s; }
.color-drops span:nth-child(34) { left: 14%; animation-duration: 13s; animation-delay: 0.6s; }
.color-drops span:nth-child(35) { left: 17%; animation-duration: 7s; animation-delay: 1.7s; }
.color-drops span:nth-child(36) { left: 21%; animation-duration: 15s; animation-delay: 0.9s; }
.color-drops span:nth-child(37) { left: 24%; animation-duration: 8s; animation-delay: 2.2s; }
.color-drops span:nth-child(38) { left: 27%; animation-duration: 12s; animation-delay: 1.1s; }
.color-drops span:nth-child(39) { left: 31%; animation-duration: 10s; animation-delay: 0.4s; }
.color-drops span:nth-child(40) { left: 34%; animation-duration: 14s; animation-delay: 1.9s; }

@keyframes drop {
  to {
    transform: translateY(calc(100vh + 200px));
  }
}

.btn-toolbar {
  display: flex;
  flex-wrap: wrap;
}

.admin-header {
  background: rgb(9 0 67 / 68%);
  padding: 1.5rem;
  border-radius: 10px;
}

.admin-container {
  padding: 4px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.admin-container-inner {
  background: #090043;
  border-radius: 12px;
  overflow: hidden;
}

.admin-content-header {
  background: linear-gradient(135deg, rgba(240, 189, 30, 0.1), rgba(204, 19, 181, 0.1));
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-content-body {
  background: #090043;
}

.table-custom {
  background: transparent;
  color: white;
  border: none;
}

.table-header-custom {
  background: linear-gradient(135deg, rgba(240, 189, 30, 0.2), rgba(204, 19, 181, 0.2));
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
}

.table-header-custom th {
  border: none;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
}

.question-row {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.question-row:hover {
  background: linear-gradient(135deg, rgba(240, 189, 30, 0.1), rgba(204, 19, 181, 0.1));
  transform: translateY(-1px);
}

.question-row td {
  border: none;
  vertical-align: middle;
}

.position-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  font-size: 0.85rem;
}

.btn-gradient {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border: none;
  color: white;
  font-weight: 600;
  padding: 10px 24px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(240, 189, 30, 0.4);
  color: white;
}

.btn-danger-custom {
  background: linear-gradient(135deg, #dc3545, #c82333);
  border: none;
  color: white;
  font-weight: 600;
  padding: 10px 24px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-danger-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4);
  color: white;
}

.btn-warning-custom {
  background: linear-gradient(135deg, #ffc107, #e0a800);
  border: none;
  color: #212529;
  font-weight: 600;
  padding: 10px 24px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-warning-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 193, 7, 0.4);
  color: #212529;
}

.btn-secondary-custom {
  background: linear-gradient(135deg, #6c757d, #5a6268);
  border: none;
  color: white;
  font-weight: 600;
  padding: 10px 24px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-secondary-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(108, 117, 125, 0.4);
  color: white;
}

.btn-outline-warning {
  border: 2px solid #ffc107;
  color: #ffc107;
  background: #090043;
  transition: all 0.3s ease;
}

.btn-outline-warning:hover {
  background: #ffc107;
  color: #212529;
  transform: translateY(-1px);
}

.btn-outline-danger {
  border: 2px solid #dc3545;
  color: #dc3545;
  background: #090043;
  transition: all 0.3s ease;
}

.btn-outline-danger:hover {
  background: #dc3545;
  color: white;
  transform: translateY(-1px);
}

.btn-outline-light {
  border: 2px solid rgba(255, 255, 255, 0.6);
  color: rgba(255, 255, 255, 0.8);
  background: #090043;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateY(-1px);
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

@media (max-width: 768px) {
  .btn-toolbar {
    flex-direction: column;
    gap: 0.5rem !important;
  }
  
  .btn-toolbar .btn {
    width: 100%;
  }
  
  .table-responsive {
    font-size: 0.875rem;
  }
  
  .admin-container {
    padding: 2px;
  }
}
</style>
