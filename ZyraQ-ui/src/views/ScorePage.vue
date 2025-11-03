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
  <div class="color-drops">
    <span v-for="n in 40" :key="n"></span>
  </div>
  <div class="container mt-5 mb-5 pb-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="score-container">
          <div class="score-container-inner text-center p-5">
            <div class="success-icon mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" fill="currentColor" class="bi bi-check-circle-fill" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
              </svg>
            </div>
            
            <h1 class="text-white mb-3">Quiz Terminé</h1>
            <p class="lead text-white-50 mb-4">{{ playerName }}</p>
            
            <div class="score-display-wrapper my-5">
              <div class="score-display">
                <div class="score-number">{{ score }}</div>
                <div class="score-label">points</div>
              </div>
            </div>

            <div v-if="score >= 8" class="alert alert-success-custom border-0" role="alert">
              <strong>Excellent !</strong> Tu maîtrises bien le sujet
            </div>
            <div v-else-if="score >= 5" class="alert alert-info-custom border-0" role="alert">
              <strong>Pas mal !</strong> Tu as de bonnes bases
            </div>
            <div v-else class="alert alert-warning-custom border-0" role="alert">
              <strong>Continue !</strong> Tu vas progresser
            </div>

            <div class="d-grid gap-3 mt-4">
              <button
                type="button"
                class="btn btn-gradient btn-lg"
                @click="restartQuiz"
              >
                Recommencer
              </button>
              <button
                type="button"
                class="btn btn-outline-light"
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
/* Animation des gouttes de couleur */
.color-drops {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.color-drops::before,
.color-drops::after {
  content: '';
  position: absolute;
  top: -10%;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  animation: fall 3s linear infinite;
}

.color-drops::before {
  background: red;
  left: 25%;
  animation-delay: 0s;
}

.color-drops::after {
  background: limegreen;
  left: 60%;
  animation-delay: 2s;
}

@keyframes fall {
  0% {
    transform: translateY(-10%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translateY(110vh) scale(0.8);
    opacity: 0;
  }
}

.color-drops span {
  position: absolute;
  top: -10%;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: fall 6s linear infinite;
}

.color-drops span:nth-child(1) {
  left: 10%;
  background: #ff006e;
  animation-delay: 1s;
}

.color-drops span:nth-child(2) {
  left: 40%;
  background: #00ff88;
  animation-delay: 2.5s;
}

.color-drops span:nth-child(3) {
  left: 70%;
  background: #00b4d8;
  animation-delay: 3.2s;
}

.color-drops span:nth-child(4) {
  left: 85%;
  background: #ffbe0b;
  animation-delay: 4s;
}

/* Conteneur principal */
.score-container {
  background: linear-gradient(90deg, #f0bd1e, #cc13b5);
  padding: 9px;
  border-radius: 39px;
  animation: slideIn 0.5s ease-out;
}

.score-container-inner {
  background-color: #090043;
  border-radius: 30px;
  width: 100%;
  height: 100%;
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
  color: #f0bd1e;
}

.score-display-wrapper {
  position: relative;
}

.score-display {
  display: inline-block;
  padding: 2rem 3rem;
  background: linear-gradient(90deg, #f0bd1e, #cc13b5);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(240, 189, 30, 0.3);
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

/* Boutons */
.btn-gradient {
  background: linear-gradient(90deg, #f0bd1e, #cc13b5);
  border: none;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  background: linear-gradient(90deg, #cc13b5, #f0bd1e);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(204, 19, 181, 0.3) !important;
  color: white;
}

.btn-outline-light {
  border: 2px solid rgba(255, 255, 255, 0.6);
  color: rgba(255, 255, 255, 0.8);
  background: #090043;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: white;
  color: white;
}

/* Alerts personnalisées */
.alert-success-custom {
  background: linear-gradient(135deg, #00ff88, #00d377);
  color: white;
  border-radius: 15px;
}

.alert-info-custom {
  background: linear-gradient(135deg, #00b4d8, #0077b6);
  color: white;
  border-radius: 15px;
}

.alert-warning-custom {
  background: linear-gradient(135deg, #ffbe0b, #fb8500);
  color: white;
  border-radius: 15px;
}
</style>
