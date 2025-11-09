<script setup>
import { ref, onMounted, computed } from 'vue';
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

function getMessageClass() {
  if (score.value >= 8) return 'message-excellent';
  if (score.value >= 5) return 'message-good';
  return 'message-keep-going';
}

function getMessageTitle() {
  if (score.value >= 8) return 'Excellent !';
  if (score.value >= 5) return 'Pas mal !';
  return 'Continue !';
}

function getMessageText() {
  if (score.value >= 8) return 'Tu maîtrises parfaitement le sujet. Bravo !';
  if (score.value >= 5) return 'Tu as de bonnes bases, continue comme ça.';
  return 'Tu vas progresser, ne lâche rien !';
}

function getCircleProgress() {
  const totalQuestions = 10;
  const circumference = 2 * Math.PI * 95;
  const progress = (score.value / totalQuestions) * circumference;
  return circumference - progress;
}
</script>

<template>
  <div class="score-page-wrapper">
    <div class="container-fluid px-4 py-5">
      <div class="score-layout">
        <div class="main-score-card contner">
          <div class="contner-inner">
            <div class="score-content text-center">
              <h1 class="completion-title text-white mb-2">Quiz Terminé !</h1>
              <p class="player-name-display text-white-50 mb-5">{{ playerName }}</p>

              <div class="score-circle-wrapper mb-5">
                <div class="score-circle">
                  <svg class="progress-ring" width="220" height="220">
                    <circle
                      class="progress-ring-bg"
                      cx="110"
                      cy="110"
                      r="95"
                    />
                    <circle
                      class="progress-ring-progress"
                      cx="110"
                      cy="110"
                      r="95"
                      :style="{ strokeDashoffset: getCircleProgress() }"
                    />
                  </svg>
                  <div class="score-inner">
                    <div class="score-number-large">{{ score }}</div>
                    <div class="score-total-label">points</div>
                  </div>
                </div>
              </div>

              <div class="message-card" :class="getMessageClass()">
                <h3 class="message-title">{{ getMessageTitle() }}</h3>
                <p class="message-text">{{ getMessageText() }}</p>
              </div>

              <div class="action-buttons mt-5">
                <button class="btn btn-gradient btn-lg px-5 mb-3" @click="restartQuiz">
                  Recommencer
                </button>
                <button class="btn btn-outline-light btn-lg px-5" @click="goHome">
                  Retour à l'accueil
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.score-page-wrapper {
  min-height: calc(100vh - 200px);
  position: relative;
  display: flex;
  align-items: center;
}

.score-layout {
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
}

.contner {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  padding: 4px;
  border-radius: 35px;
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.contner-inner {
  background-color: #090043;
  padding: 4rem 3rem;
  border-radius: 31px;
  position: relative;
  overflow: hidden;
}

.score-content {
  position: relative;
  z-index: 1;
}

.completion-title {
  font-size: 2.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.player-name-display {
  font-size: 1.3rem;
  font-weight: 500;
}

.score-circle-wrapper {
  display: flex;
  justify-content: center;
  animation: fadeIn 1s ease-out 0.3s both;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.score-circle {
  position: relative;
  width: 220px;
  height: 220px;
}

.progress-ring {
  transform: rotate(-90deg);
}

.progress-ring-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.1);
  stroke-width: 12;
}

.progress-ring-progress {
  fill: none;
  stroke: url(#gradient);
  stroke-width: 12;
  stroke-linecap: round;
  stroke-dasharray: 596.9;
  transition: stroke-dashoffset 1.5s ease-out;
}

.score-inner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.score-number-large {
  font-size: 4rem;
  font-weight: 800;
  color: #f0bd1e;
  line-height: 1;
  text-shadow: 0 0 30px rgba(240, 189, 30, 0.5);
}

.score-total-label {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-top: 0.5rem;
}

.message-card {
  padding: 2rem;
  border-radius: 20px;
  margin: 2rem auto;
  max-width: 500px;
  animation: slideIn 1s ease-out 0.5s both;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.message-excellent {
  background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(0, 211, 119, 0.15));
  border: 2px solid rgba(0, 255, 136, 0.3);
}

.message-good {
  background: linear-gradient(135deg, rgba(0, 180, 216, 0.15), rgba(0, 119, 182, 0.15));
  border: 2px solid rgba(0, 180, 216, 0.3);
}

.message-keep-going {
  background: linear-gradient(135deg, rgba(255, 190, 11, 0.15), rgba(251, 133, 0, 0.15));
  border: 2px solid rgba(255, 190, 11, 0.3);
}

.message-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  margin-bottom: 0.5rem;
}

.message-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.1rem;
  margin: 0;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  animation: fadeIn 1.2s ease-out 0.7s both;
}

.btn-gradient {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border: none;
  color: white;
  font-weight: 700;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-gradient:hover {
  background: linear-gradient(135deg, #cc13b5, #f0bd1e);
  transform: translateY(-3px);
  box-shadow: 0 10px 35px rgba(240, 189, 30, 0.5) !important;
  color: white;
}

.btn-outline-light {
  border: 2px solid rgba(255, 255, 255, 0.4);
  color: rgba(255, 255, 255, 0.8);
  background: transparent;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
  color: white;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .contner-inner {
    padding: 3rem 2rem;
  }
  
  .completion-title {
    font-size: 2.2rem;
  }
  
  .score-circle {
    width: 180px;
    height: 180px;
  }
  
  .score-number-large {
    font-size: 3rem;
  }
  
  .message-title {
    font-size: 1.5rem;
  }
}
</style>
