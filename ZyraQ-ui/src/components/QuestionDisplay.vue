<script setup>
const props = defineProps({
  question: Object,
  selectedAnswer: Number,
  showNextButton: Boolean,
});

const emit = defineEmits(['answer-clicked', 'next-question']);

function selectAnswer(answerIndex) {
  emit('answer-clicked', answerIndex);
}

function goToNextQuestion() {
  emit('next-question');
}
</script>

<template>
  <div class="question-wrapper" v-if="question">
    <div class="question-container">
      <div class="question-container-inner">
        <div class="question-grid">
          <div class="question-section">
            <div class="question-header mb-4">
              <span class="badge bg-gradient">Question {{ question.position }}</span>
            </div>

            <h2 class="question-title text-white mb-4">{{ question.title }}</h2>
            <h3 class="question-text text-white-75 mb-4">{{ question.text }}</h3>

            <div v-if="question.image" class="question-image-wrapper">
              <div class="image-container">
                <img
                  :src="question.image"
                  alt="Image de la question"
                  class="img-fluid rounded"
                />
              </div>
            </div>
          </div>

          <div class="answers-section">
            <div class="answers-header mb-4">
              <h4 class="text-white mb-0">
                Choisissez votre réponse
              </h4>
            </div>

            <div class="answers-list">
              <button
                v-for="(answer, index) in question.possibleAnswers"
                :key="index"
                @click="selectAnswer(index + 1)"
                class="answer-card"
                :class="{
                  selected: selectedAnswer === index + 1,
                }"
              >
                <div class="answer-header">
                  <span class="answer-letter">{{ String.fromCharCode(65 + index) }}</span>
                </div>
                <p class="answer-text">{{ answer }}</p>
              </button>
            </div>

            <div v-if="showNextButton" class="next-button-wrapper">
              <button @click="goToNextQuestion" class="next-question-btn">
                Question Suivante →
              </button>
            </div>
          </div>
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
.question-wrapper {
  width: 100%;
  max-width: 1800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.question-container {
  padding: 4px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}

.question-container-inner {
  background: #090043;
  border-radius: 20px;
  overflow: hidden;
  padding: 3rem;
}

.question-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 3rem;
  align-items: start;
}

@media (max-width: 992px) {
  .question-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}

.question-section {
  position: sticky;
  top: 2rem;
}

.question-header {
  margin-bottom: 1.5rem;
}

.bg-gradient {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5) !important;
  color: white;
  font-weight: 700;
  padding: 10px 20px;
  border-radius: 12px;
  border: none;
  font-size: 1rem;
  display: inline-block;
}

.question-title {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1.3;
  margin-bottom: 1.5rem;
}

.question-text {
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.text-white-75 {
  color: rgba(255, 255, 255, 0.75);
}

.question-image-wrapper {
  margin-top: 2rem;
}

.image-container {
  padding: 4px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 16px;
  overflow: hidden;
}

.image-container img {
  border-radius: 12px;
  display: block;
  width: 100%;
  height: auto;
  max-height: 500px;
  object-fit: cover;
}

.answers-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.answers-header {
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.answers-header h4 {
  display: flex;
  align-items: center;
  font-size: 1.3rem;
  font-weight: 600;
}

.answers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.answer-card {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  position: relative;
  overflow: hidden;
}

.answer-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.answer-card:hover {
  border-color: rgba(240, 189, 30, 0.5);
  background: rgba(240, 189, 30, 0.08);
  transform: translateX(8px);
}

.answer-card:hover::before {
  opacity: 1;
}

.answer-card.selected {
  border-color: #f0bd1e;
  background: linear-gradient(135deg, rgba(240, 189, 30, 0.15), rgba(204, 19, 181, 0.15));
  box-shadow: 0 8px 25px rgba(240, 189, 30, 0.3);
  transform: translateX(8px);
}

.answer-card.selected::before {
  opacity: 1;
  width: 6px;
}

.answer-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: 0.75rem;
}

.answer-letter {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  color: white;
  border-radius: 12px;
  font-weight: 800;
  font-size: 1.3rem;
  flex-shrink: 0;
}

.answer-card.selected .answer-letter {
  background: linear-gradient(135deg, #48bb78, #38a169);
  box-shadow: 0 0 20px rgba(72, 187, 120, 0.6);
  animation: bounce 0.5s ease;
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.answer-text {
  color: white;
  font-size: 1.05rem;
  font-weight: 500;
  line-height: 1.5;
  margin: 0;
}

.next-button-wrapper {
  margin-top: 1rem;
  padding-top: 1.5rem;
  border-top: 2px solid rgba(255, 255, 255, 0.1);
}

.next-question-btn {
  width: 100%;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  color: white;
  border: none;
  padding: 1.25rem 2rem;
  border-radius: 14px;
  font-size: 1.15rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(240, 189, 30, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.next-question-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 35px rgba(240, 189, 30, 0.6);
  background: linear-gradient(135deg, #cc13b5, #f0bd1e);
}

.alert-container {
  padding: 4px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  max-width: 600px;
  margin: 3rem auto;
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
  padding: 2rem;
  margin: 1rem;
  backdrop-filter: blur(10px);
}

@media (max-width: 768px) {
  .question-container-inner {
    padding: 1.5rem;
  }
  
  .question-title {
    font-size: 1.6rem;
  }
  
  .question-text {
    font-size: 1rem;
  }
  
  .answer-card {
    padding: 1.25rem;
  }
  
  .answer-letter {
    width: 38px;
    height: 38px;
    font-size: 1.1rem;
  }
  
  .answer-text {
    font-size: 0.95rem;
  }
  
  .next-question-btn {
    padding: 1rem 1.5rem;
    font-size: 1rem;
  }
}
</style>
