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
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-10 col-lg-8">
        <div class="progress-section mb-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h1 class="h4 text-white mb-0">Quiz en cours</h1>
            <span class="badge bg-white text-dark px-3 py-2">
              Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}
            </span>
          </div>
          <div class="progress" style="height: 8px; border-radius: 10px">
            <div
              class="progress-bar bg-white"
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

        <QuestionDisplay
          :question="currentQuestion"
          @answer-clicked="answerClickedHandler"
        />

        <div class="mt-4 text-center">
          <small class="text-white-50">
            {{ participationStorageService.getPlayerName() }}
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.progress-bar {
  transition: width 0.5s ease;
}

.badge {
  font-weight: 600;
  font-size: 0.95rem;
  letter-spacing: 0.5px;
}
</style>
