<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import QuestionDisplay from '@/components/QuestionDisplay.vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';

const router = useRouter();
const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const answers = ref([]);

onMounted(async () => {
  console.log('Questions Manager mounted');
  
  const playerName = participationStorageService.getPlayerName();
  if (!playerName) {
    console.log('No player name, redirect');
    router.push('/new-quiz');
    return;
  }

  try {
    const quizInfo = await quizApiService.getQuizInfo();
    if (quizInfo && quizInfo.data) {
      totalNumberOfQuestions.value = quizInfo.data.size || 0;
    }
  } catch (error) {
    console.error('Erreur chargement quiz:', error);
  }

  await loadQuestionByPosition(1);
});

async function loadQuestionByPosition(position) {
  try {
    console.log('Loading question:', position);
    const response = await quizApiService.getQuestion(position);
    
    if (response && response.data) {
      currentQuestion.value = response.data;
      currentQuestionPosition.value = position;
    } else {
      console.error('No data received');
    }
  } catch (error) {
    console.error('Erreur chargement question:', error);
  }
}

async function answerClickedHandler(answerIndex) {
  console.log('Answer clicked:', answerIndex);
  
  answers.value.push(answerIndex);
  participationStorageService.saveAnswers(answers.value);
  
  if (currentQuestionPosition.value >= totalNumberOfQuestions.value) {
    await endQuiz();
  } else {
    await loadQuestionByPosition(currentQuestionPosition.value + 1);
  }
}

async function endQuiz() {
  console.log('Quiz finished');
  
  try {
    const playerName = participationStorageService.getPlayerName();
    const response = await quizApiService.postParticipation(
      playerName,
      answers.value
    );
    
    if (response && response.data) {
      participationStorageService.saveParticipationScore(response.data.score);
      router.push('/score');
    }
  } catch (error) {
    console.error('Erreur envoi:', error);
    alert('Erreur lors de l\'envoi');
  }
}
</script>

<template>
  <div>
    <div class="color-drops">
      <span v-for="n in 40" :key="n"></span>
    </div>
    <div class="container mt-5 mb-5 pb-5">
      <div class="row justify-content-center">
        <div class="col-md-10 col-lg-8">
          <div class="progress-section mb-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h1 class="h4 text-white mb-0">Quiz en cours</h1>
              <span class="badge bg-gradient text-white px-3 py-2">
                Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}
              </span>
            </div>
            <div class="progress-container">
              <div class="progress-container-inner">
                <div class="progress custom-progress">
                  <div
                    class="progress-bar custom-progress-bar"
                    role="progressbar"
                    :style="{
                      width:
                        (currentQuestionPosition / totalNumberOfQuestions) * 100 + '%',
                    }"
                    :aria-valuenow="currentQuestionPosition"
                    aria-valuemin="0"
                    :aria-valuemax="totalNumberOfQuestions"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <QuestionDisplay
            :question="currentQuestion"
            @answer-clicked="answerClickedHandler"
          />

          <div class="mt-4 text-center">
            <small class="text-white-50 player-name">
              {{ participationStorageService.getPlayerName() }}
            </small>
          </div>
        </div>
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

.progress-container {
  padding: 3px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.progress-container-inner {
  background: #090043;
  border-radius: 13px;
  padding: 8px;
}

.custom-progress {
  height: 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.custom-progress-bar {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  transition: width 0.8s ease;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
}

.custom-progress-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.bg-gradient {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5) !important;
  border: none;
  font-weight: 600;
  font-size: 0.95rem;
  letter-spacing: 0.5px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(240, 189, 30, 0.3);
}

.player-name {
  background: rgba(255, 255, 255, 0.1);
  padding: 8px 16px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-weight: 500;
  letter-spacing: 0.5px;
}

@media (max-width: 768px) {
  .progress-container {
    padding: 2px;
  }
  
  .progress-container-inner {
    padding: 6px;
  }
  
  .custom-progress {
    height: 10px;
  }
  
  .bg-gradient {
    font-size: 0.85rem;
    padding: 8px 16px;
  }
}
</style>
