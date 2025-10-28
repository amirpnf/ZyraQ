<!-- QuizGame.vue -->
<script setup>
import { ref, onMounted } from 'vue';
import QuestionDisplay from './QuestionDisplay.vue';

const currentQuestion = ref(null);
const currentPosition = ref(1);
const isLoading = ref(false);
const error = ref(null);

async function fetchQuestion(position) {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await fetch(`http://localhost:5000/questions?position=${position}`);

    if (!response.ok) {
      throw new Error(`Question not found at position ${position}`);
    }

    const questionData = await response.json();
    currentQuestion.value = questionData;
  } catch (err) {
    error.value = err.message;
    currentQuestion.value = null;
  } finally {
    isLoading.value = false;
  }
}

function handleAnswerClicked(answerIndex) {
  console.log(`Answer ${answerIndex} selected for question at position ${currentPosition.value}`);

  // Move to next question
  currentPosition.value++;
  fetchQuestion(currentPosition.value);
}

function restartQuiz() {
  currentPosition.value = 1;
  fetchQuestion(1);
}

onMounted(() => {
  fetchQuestion(currentPosition.value);
});
</script>

<template>
  <div class="quiz-container">
    <!-- Centered Header -->
    <header class="text-center py-4 mb-4">
      <h1 class="quiz-title">Quiz Game</h1>
    </header>

    <div v-if="isLoading" class="loading text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading question...</p>
    </div>

    <div v-else-if="error" class="error-alert text-center">
      <div class="alert alert-warning"><strong>Quiz Completed!</strong> {{ error }}</div>
      <button @click="restartQuiz" class="btn btn-primary">Restart Quiz</button>
    </div>

    <QuestionDisplay v-else :question="currentQuestion" @answer-clicked="handleAnswerClicked" />
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
</style>
