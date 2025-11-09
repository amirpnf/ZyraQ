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
  const playerName = participationStorageService.getPlayerName();
  if (!playerName) {
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
  // recupération de la question depuis l'api
  try {
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
  // sauvegarde de la reponce
  answers.value.push(answerIndex);
  participationStorageService.saveAnswers(answers.value);
  
  if (currentQuestionPosition.value >= totalNumberOfQuestions.value) {
    await endQuiz();
  } else {
    await loadQuestionByPosition(currentQuestionPosition.value + 1);
  }
}

async function endQuiz() {
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
