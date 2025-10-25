<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';

const router = useRouter();
const playerName = ref('');
const score = ref(0);

onMounted(() => {
  playerName.value = participationStorageService.getPlayerName() || 'Joueur';
  score.value = participationStorageService.getParticipationScore() || 0;
  
  if (score.value === null) {
    router.push('/');
  }
});

function restartQuiz() {
  participationStorageService.clear();
  router.push('/new-quiz');
}

function goHome() {
  router.push('/');
}
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-lg border-0 text-center">
          <div class="card-body p-5">
            <div class="success-icon mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" fill="currentColor" class="bi bi-check-circle-fill" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
              </svg>
            </div>
            
            <h1 class="card-title mb-3">Quiz Terminé</h1>
            <p class="lead text-muted mb-4">{{ playerName }}</p>
            
            <div class="score-display-wrapper my-5">
              <div class="score-display">
                <div class="score-number">{{ score }}</div>
                <div class="score-label">points</div>
              </div>
            </div>

            <div v-if="score >= 8" class="alert alert-success border-0" role="alert">
              <strong>Excellent !</strong> Tu maîtrises bien le sujet
            </div>
            <div v-else-if="score >= 5" class="alert alert-info border-0" role="alert">
              <strong>Pas mal !</strong> Tu as de bonnes bases
            </div>
            <div v-else class="alert alert-warning border-0" role="alert">
              <strong>Continue !</strong> Tu vas progresser
            </div>

            <div class="d-grid gap-3 mt-4">
              <button
                type="button"
                class="btn btn-primary btn-lg"
                @click="restartQuiz"
              >
                Recommencer
              </button>
              <button
                type="button"
                class="btn btn-outline-secondary"
                @click="goHome"
              >
                Retour à l'accueil
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  border-radius: 20px;
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.success-icon {
  color: #667eea;
}

.score-display-wrapper {
  position: relative;
}

.score-display {
  display: inline-block;
  padding: 2rem 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.score-number {
  font-size: 4rem;
  font-weight: 700;
  color: white;
  line-height: 1;
}

.score-label {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
  margin-top: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}
</style>
