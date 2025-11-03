<!-- QuestionComponent.vue -->
<script setup>
const props = defineProps({
  question: Object,
  selectedAnswer: Number,
  showNextButton: Boolean,
});

console.log('Question Data: ', props.question);

const emit = defineEmits(['answer-clicked', 'next-question']);

function selectAnswer(answerIndex) {
  console.log('Selecting answer:', answerIndex, 'Current selected:', props.selectedAnswer);
  // Emit always (parent can ignore duplicate clicks)
  emit('answer-clicked', answerIndex);
}

function goToNextQuestion() {
  emit('next-question');
}
</script>

<template>
  <div class="question-container" v-if="question">
    <div class="question-container-inner">
      <div class="question-body p-5">
        <div class="question-header mb-3 text-center">
          <span class="badge bg-gradient fs-6">Question {{ question.position }}</span>
        </div>

        <h2 class="question-title mb-4 text-center text-white">{{ question.title }}</h2>

        <h3 class="question-text mb-4 text-center text-white-75">{{ question.text }}</h3>

        <div v-if="question.image" class="text-center mb-4">
          <div class="image-container">
            <img
              :src="question.image"
              alt="Question image"
              class="img-fluid rounded shadow-sm"
              style="max-height: 300px"
            />
          </div>
        </div>

        <!-- Answers Section -->
        <div class="answers-grid">
          <button
            v-for="(answer, index) in question.possibleAnswers"
            :key="index"
            @click="selectAnswer(index + 1)"
            class="answer-btn"
            :class="{
              selected: selectedAnswer === index + 1,
              }"
          >
            <span class="answer-letter">{{ String.fromCharCode(65 + index) }}</span>
            <span class="answer-text">{{ answer }}</span>
          </button>
        </div>

        <!-- Next Question Button -->
        <div v-if="showNextButton" class="next-button-container text-center mt-4">
          <button @click="goToNextQuestion" class="next-question-btn">Question Suivante →</button>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="alert-container">
    <div class="alert-container-inner">
      <div class="alert alert-warning-custom border-0 text-center">
        <strong>Attention:</strong> Pas de question disponible
      </div>
    </div>
  </div>
</template>

<style scoped>
.question-container {
  padding: 4px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.question-container-inner {
  background: #090043;
  border-radius: 12px;
  overflow: hidden;
}

.question-body {
  background: #090043;
}

.question-header {
  margin-bottom: 1.5rem;
}

.bg-gradient {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5) !important;
  color: white;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
}

.question-title {
  font-size: 1.8rem;
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: 1.5rem;
}

.question-text {
  font-size: 1.3rem;
  font-weight: 500;
  line-height: 1.4;
  margin-bottom: 2rem;
}

.text-white-75 {
  color: rgba(255, 255, 255, 0.75);
}

.image-container {
  padding: 3px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 12px;
  display: inline-block;
}

.image-container img {
  border-radius: 9px;
  display: block;
}

.answers-grid {
  display: grid;
  gap: 1rem;
  margin-top: 2rem;
}

.answer-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  text-align: left;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 1rem;
  color: white;
  backdrop-filter: blur(10px);
}

.answer-btn:hover {
  border-color: rgba(240, 189, 30, 0.6);
  background: rgba(240, 189, 30, 0.1);
  transform: translateX(8px);
  box-shadow: 0 4px 20px rgba(240, 189, 30, 0.3);
}

.answer-btn.selected {
  border-color: #f0bd1e;
  background: linear-gradient(135deg, rgba(240, 189, 30, 0.2), rgba(204, 19, 181, 0.2));
  box-shadow: 0 4px 20px rgba(240, 189, 30, 0.4);
  transform: translateX(8px);
}

.answer-btn.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.answer-btn.disabled:hover {
  transform: none;
  border-color: rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.05);
  box-shadow: none;
}

.answer-letter {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  color: white;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.answer-btn.selected .answer-letter {
  background: linear-gradient(135deg, #48bb78, #38a169);
  box-shadow: 0 0 15px rgba(72, 187, 120, 0.5);
}

.answer-text {
  flex: 1;
  font-weight: 500;
}

.next-button-container {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 2px solid rgba(255, 255, 255, 0.1);
}

.next-question-btn {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  color: white;
  border: none;
  padding: 1rem 2.5rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(240, 189, 30, 0.3);
}

.next-question-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(240, 189, 30, 0.5);
}

.alert-container {
  padding: 4px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.alert-container-inner {
  background: #090043;
  border-radius: 12px;
  overflow: hidden;
}

.alert-warning-custom {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem;
  backdrop-filter: blur(10px);
}

@media (max-width: 768px) {
  .question-container {
    padding: 2px;
  }
  
  .question-title {
    font-size: 1.5rem;
  }
  
  .question-text {
    font-size: 1.1rem;
  }
  
  .answer-btn {
    padding: 1rem;
    font-size: 0.9rem;
  }
  
  .answer-letter {
    width: 35px;
    height: 35px;
    font-size: 1rem;
  }
  
  .next-question-btn {
    padding: 0.875rem 2rem;
    font-size: 1rem;
  }
}
</style>
