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
  <div class="page-wrapper">
    <div class="container-fluid px-4 py-4">
      <div class="admin-top-bar mb-4">
        <div class="top-bar-inner">
          <h1 class="admin-title">Gestion des Questions</h1>
          <button @click="logout" class="btn-logout">
            Déconnexion
          </button>
        </div>
      </div>

      <div class="admin-layout">
        <aside class="admin-sidebar">
          <div class="sidebar-card contner">
            <div class="contner-inner">
              <h3 class="sidebar-title text-white mb-4">Actions rapides</h3>
              
              <button @click="createQuestion" class="sidebar-btn btn-gradient mb-3">
                + Créer une question
              </button>

              <div class="stats-box mb-4">
                <div class="stat-item">
                  <span class="stat-label">Total</span>
                  <span class="stat-value">{{ questions.length }}</span>
                </div>
              </div>

              <div class="danger-zone">
                <h4 class="danger-title text-white mb-3">Zone dangereuse</h4>
                <button @click="deleteAllParticipations" class="sidebar-btn btn-warning-custom mb-2">
                  Supprimer participations
                </button>
                <button @click="deleteAllQuestions" class="sidebar-btn btn-danger-custom mb-2">
                  Supprimer questions
                </button>
                <button @click="rebuildDatabase" class="sidebar-btn btn-secondary-custom">
                  Reconstruire BDD
                </button>
              </div>
            </div>
          </div>

          <router-link to="/" class="btn-back-home">
            Retour à l'accueil
          </router-link>
        </aside>

        <main class="admin-main-content">
          <div v-if="isLoading" class="loading-state">
            <div class="spinner-border text-light" role="status">
              <span class="visually-hidden">Chargement...</span>
            </div>
            <p class="text-white-50 mt-3">Chargement des questions...</p>
          </div>

          <div v-else-if="questions.length === 0" class="empty-state contner">
            <div class="contner-inner text-center py-5">
              <h3 class="text-white mb-2">Aucune question</h3>
              <p class="text-white-50 mb-4">Commence par créer ta première question</p>
              <button @click="createQuestion" class="btn btn-gradient">
                Créer une question
              </button>
            </div>
          </div>

          <div v-else class="questions-grid">
            <div v-for="q in questions" :key="q.id" class="question-card contner">
              <div class="contner-inner">
                <div class="question-card-header">
                  <div class="question-position">{{ q.position }}</div>
                  <div class="question-id">#{{ q.id }}</div>
                </div>
                <div class="question-card-body">
                  <h4 class="question-title text-white">{{ q.text }}</h4>
                </div>
                <div class="question-card-actions">
                  <button @click="editQuestion(q.id)" class="btn-edit">
                    Modifier
                  </button>
                  <button @click="deleteQuestion(q.id)" class="btn-delete">
                    Supprimer
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  position: relative;
  background: #090043;
}

.contner {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  padding: 3px;
  border-radius: 20px;
  position: relative;
  z-index: 1;
}

.contner-inner {
  background-color: #090043;
  padding: 1.5rem;
  border-radius: 17px;
  width: 100%;
  height: 100%;
}

.admin-top-bar {
  position: relative;
  z-index: 1;
}

.top-bar-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, rgba(240, 189, 30, 0.15), rgba(204, 19, 181, 0.15));
  backdrop-filter: blur(10px);
  padding: 1.5rem 2rem;
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.admin-title {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.btn-logout {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: white;
  transform: translateY(-2px);
}

.admin-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 2rem;
  margin-top: 2rem;
  position: relative;
  z-index: 1;
}

.admin-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sidebar-card {
  position: sticky;
  top: 1rem;
}

.sidebar-title {
  font-size: 1.25rem;
  font-weight: 700;
}

.sidebar-btn {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.btn-gradient {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  color: white;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(240, 189, 30, 0.4);
}

.stats-box {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.danger-zone {
  padding-top: 1rem;
  border-top: 2px solid rgba(255, 255, 255, 0.1);
}

.danger-title {
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.8;
}

.btn-warning-custom {
  background: linear-gradient(135deg, #ffc107, #e0a800);
  color: #212529;
}

.btn-warning-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 193, 7, 0.4);
}

.btn-danger-custom {
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: white;
}

.btn-danger-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(220, 53, 69, 0.4);
}

.btn-secondary-custom {
  background: linear-gradient(135deg, #6c757d, #5a6268);
  color: white;
}

.btn-secondary-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(108, 117, 125, 0.4);
}

.btn-back-home {
  display: block;
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-back-home:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
  color: white;
  transform: translateY(-2px);
}

/* Contenu principal */
.admin-main-content {
  min-height: 600px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 5rem 0;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

.empty-state {
  margin-top: 3rem;
}

.empty-icon {
  font-size: 4rem;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.question-card {
  transition: all 0.3s ease;
}

.question-card:hover {
  transform: translateY(-5px);
}

.question-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-position {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 50%;
  font-weight: 800;
  font-size: 1.25rem;
  color: white;
}

.question-id {
  color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
  font-size: 0.9rem;
}

.question-card-body {
  margin-bottom: 1.5rem;
  min-height: 80px;
}

.question-title {
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.4;
  margin: 0;
}

.question-card-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-edit,
.btn-delete {
  padding: 0.75rem;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid;
}

.btn-edit {
  background: rgba(255, 193, 7, 0.1);
  border-color: #ffc107;
  color: #ffc107;
}

.btn-edit:hover {
  background: #ffc107;
  color: #212529;
  transform: translateY(-2px);
}

.btn-delete {
  background: rgba(220, 53, 69, 0.1);
  border-color: #dc3545;
  color: #dc3545;
}

.btn-delete:hover {
  background: #dc3545;
  color: white;
  transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 1200px) {
  .admin-layout {
    grid-template-columns: 280px 1fr;
  }
  
  .questions-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 992px) {
  .admin-layout {
    grid-template-columns: 1fr;
  }
  
  .sidebar-card {
    position: static;
  }
  
  .questions-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .admin-title {
    font-size: 1.5rem;
  }
  
  .top-bar-inner {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .questions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
