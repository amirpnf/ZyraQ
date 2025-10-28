<!-- QuestionComponent.vue -->
<script setup>
const props = defineProps({
  question: Object,
})

const emit = defineEmits(['answer-clicked'])

function selectAnswer(answerIndex) {
  emit('answer-clicked', answerIndex)
}
</script>

<template>
  <div class="card shadow-lg border-0" v-if="question">
    <div class="card-body p-5">
      <!-- Centered Question Position -->
      <div class="question-header mb-3 text-center">
        <span class="badge bg-primary fs-6">Question {{ question.position }}</span>
      </div>
      
      <!-- Centered Question Title -->
      <h2 class="question-title mb-4 text-center">{{ question.title }}</h2>
      
      <!-- Centered Question Text -->
      <h3 class="question-text mb-4 text-center">{{ question.text }}</h3>
      
      <div v-if="question.image" class="text-center mb-4">
        <img 
          :src="question.image" 
          alt="Question image" 
          class="img-fluid rounded shadow-sm" 
          style="max-height: 300px" 
        />
      </div>
      
      <div class="answers-grid">
        <button 
          v-for="(answer, index) in question.possibleAnswers" 
          :key="index" 
          @click="selectAnswer(index + 1)" 
          class="answer-btn"
        >
          <span class="answer-letter">{{ String.fromCharCode(65 + index) }}</span>
          <span class="answer-text">{{ answer }}</span>
        </button>
      </div>
    </div>
  </div>
  
  <div v-else class="alert alert-warning border-0 shadow-sm text-center">
    <strong>Attention:</strong> Pas de question disponible
  </div>
</template>

<style scoped>
.card {
  border-radius: 15px;
}

.question-header {
  margin-bottom: 1.5rem;
}

.question-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2d3748;
  line-height: 1.4;
  margin-bottom: 1.5rem;
}

.question-text {
  font-size: 1.3rem;
  font-weight: 500;
  color: #4a5568;
  line-height: 1.4;
  margin-bottom: 2rem;
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
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  text-align: left;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 1rem;
  color: #2d3748;
}

.answer-btn:hover {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  transform: translateX(8px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.answer-letter {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.answer-text {
  flex: 1;
  font-weight: 500;
}

/* Ensure text-center class works */
.text-center {
  text-align: center;
}
</style>