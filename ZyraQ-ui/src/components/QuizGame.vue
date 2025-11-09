<script setup>
import { ref, onMounted } from 'vue';
import QuestionDisplay from './QuestionDisplay.vue';

const currentQuestion = ref(null);
const currentPosition = ref(1);
const isLoading = ref(false);
const error = ref(null);
const selectedAnswer = ref(0);
const showNextButton = ref(false);

async function fetchQuestion(position) {
  isLoading.value = true;
  error.value = null;
  selectedAnswer.value = 0;
  showNextButton.value = false;

  try {
    const response = await fetch(`http://localhost:5000/questions?position=${position}`);
    if (!response.ok) {
      return null;
    }
    const questionData = await response.json();
    return questionData;
  } catch (err) {
    console.error('Fetch error:', err);
    return null;
  } finally {
    isLoading.value = false;
  }
}

async function loadQuestion(startPos) {
  let pos = startPos;
  let question = null;

  while (!question) {
    question = await fetchQuestion(pos);
    if (!question) {
      pos++;
      if (pos > 1000) {
        break;
      }
    }
  }

  if (question) {
    currentQuestion.value = question;
    currentPosition.value = question.position;
    selectedAnswer.value = 0;
    showNextButton.value = false;
  } else {
    currentQuestion.value = null;
    error.value = 'Quiz terminé !';
  }
}

function handleAnswerClicked(answerIndex) {
  selectedAnswer.value = answerIndex;
  showNextButton.value = true;
}

async function nextQuestion() {
  let pos = currentPosition.value + 1;
  let question = null;

  while (!question) {
    try {
      const response = await fetch(`http://localhost:5000/questions?position=${pos}`);
      if (!response.ok) throw new Error('Question not found');

      question = await response.json();
      currentQuestion.value = question;
      currentPosition.value = question.position;
      selectedAnswer.value = 0;
      showNextButton.value = false;
    } catch (err) {
      pos++;
      if (pos > 1000) {
        currentQuestion.value = null;
        error.value = 'Quiz terminé !';
        return;
      }
    }
  }
}

function restartQuiz() {
  error.value = null;
  loadQuestion(1);
}

onMounted(() => {
  loadQuestion(1);
});
</script>

<template>
  <div class="quiz-container">
    <header class="text-center py-4 mb-4">
      <h1 class="quiz-title">ZyraQ Quiz</h1>
    </header>

    <div v-if="isLoading" class="loading text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
      <p>Chargement de la question...</p>
    </div>

    <div v-else-if="error" class="error-alert text-center">
      <div class="alert alert-warning"><strong>Quiz Terminé !</strong> {{ error }}</div>
      <button @click="restartQuiz" class="btn btn-primary">Recommencer</button>
    </div>

    <QuestionDisplay
      v-else
      :question="currentQuestion"
      :selected-answer="selectedAnswer"
      :show-next-button="showNextButton"
      @answer-clicked="handleAnswerClicked"
      @next-question="nextQuestion"
    />

    <div class="debug-info mt-3 p-3 bg-light rounded">
      <small>
        Info: selectedAnswer = {{ selectedAnswer }}, showNextButton = {{ showNextButton }},
        currentPosition = {{ currentPosition }}
      </small>
    </div>
  </div>
</template>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.quiz-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0;
}

.loading {
  padding: 2rem;
}

.error-alert {
  padding: 2rem;
}

.debug-info {
  font-family: monospace;
  background: #f8f9fa;
  border-left: 4px solid #dc3545;
}
</style>
