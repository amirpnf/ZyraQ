<!-- QuizGame.vue -->
<script setup>
import { ref, onMounted } from 'vue';
import QuestionDisplay from './QuestionDisplay.vue';

const currentQuestion = ref(null);
const currentPosition = ref(1);
const isLoading = ref(false);
const error = ref(null);
const selectedAnswer = ref(0);
const showNextButton = ref(false);

/**
 * Fetch a question by position.
 * Returns the question object, or null if not found.
 */
async function fetchQuestion(position) {
  isLoading.value = true;
  error.value = null;
  selectedAnswer.value = 0;
  showNextButton.value = false;

  try {
    const response = await fetch(`http://localhost:5000/questions?position=${position}`);
    if (!response.ok) {
      return null; // Question not found
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

/**
 * Load the first question or next available question starting from `startPos`.
 */
async function loadQuestion(startPos) {
  let pos = startPos;
  let question = null;

  // Keep trying next positions until a question is found or max position reached
  while (!question) {
    question = await fetchQuestion(pos);
    if (!question) {
      pos++;
      if (pos > 1000) {
        // arbitrary large number to avoid infinite loop
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

// Handle answer clicked
function handleAnswerClicked(answerIndex) {
  selectedAnswer.value = answerIndex;
  showNextButton.value = true;
  console.log(`Answer ${answerIndex} selected for question at position ${currentPosition.value}`);
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
      pos++; // skip to next position
      if (pos > 1000) {
        // safety stop
        currentQuestion.value = null;
        error.value = 'Quiz terminé !';
        return;
      }
    }
  }
}

// Restart the quiz
function restartQuiz() {
  error.value = null;
  loadQuestion(1);
}

// Load first question on mount
onMounted(() => {
  loadQuestion(1);
});
</script>

<template>
  <div class="quiz-container">
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

    <QuestionDisplay
      v-else
      :question="currentQuestion"
      :selected-answer="selectedAnswer"
      :show-next-button="showNextButton"
      @answer-clicked="handleAnswerClicked"
      @next-question="nextQuestion"
    />

    <!-- Debug info -->
    <div class="debug-info mt-3 p-3 bg-light rounded">
      <small>
        Debug: selectedAnswer = {{ selectedAnswer }}, showNextButton = {{ showNextButton }},
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
