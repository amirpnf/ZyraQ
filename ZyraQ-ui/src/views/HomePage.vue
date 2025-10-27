<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';

const registeredScores = ref([]);
const totalQuestions = ref(0);

onMounted(async () => {
  console.log('Home mounted');
  try {
    const response = await quizApiService.getQuizInfo();
    if (response && response.data) {
      registeredScores.value = response.data.scores || [];
      totalQuestions.value = response.data.size || 0;
    }
  } catch (error) {
    console.error('Erreur chargement quiz:', error);
  }
});

function getRankClass(index) {
  if (index === 0) return 'rank-gold';
  if (index === 1) return 'rank-silver';
  if (index === 2) return 'rank-bronze';
  return '';
}
</script>

<template>
  <div class="color-drops">
    <span v-for="n in 40" :key="n"></span>
  </div>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-10 col-lg-8">
        <div class="hero-section text-center mb-5">
          <h1 class="display-3 fw-bold text-white mb-3">ZyraQ Quiz</h1>
          <p class="lead text-white-50 mb-4">
            Test tes connaissances avec {{ totalQuestions }} questions
          </p>
          <router-link to="/new-quiz" class="btn btn-light btn-lg px-5 py-3 shadow">
            Démarrer le Quiz
          </router-link>
        </div>

        <div class="card shadow-lg border-0">
          <div class="card-header bg-white border-0 py-4">
            <h2 class="h4 mb-0 text-dark text-center">Tableau des Scores</h2>
          </div>
          <div class="card-body p-0">
            <div v-if="registeredScores.length === 0" class="text-center py-5">
              <p class="text-muted mb-0">Pas encore de scores. Sois le premier !</p>
            </div>
            <div v-else class="table-responsive">
              <table class="table table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th class="px-4 py-3">Rang</th>
                    <th class="px-4 py-3">Joueur</th>
                    <th class="px-4 py-3 text-end">Score</th>
                    <th class="px-4 py-3 text-end">Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(scoreEntry, index) in registeredScores"
                    :key="scoreEntry.date"
                    class="score-row"
                  >
                    <td class="px-4 py-3">
                      <span class="rank-badge" :class="getRankClass(index)">
                        {{ index + 1 }}
                      </span>
                    </td>
                    <td class="px-4 py-3 fw-semibold">{{ scoreEntry.playerName }}</td>
                    <td class="px-4 py-3 text-end">
                      <span class="score-value">
                        {{ scoreEntry.score }} / {{ totalQuestions }}
                      </span>
                    </td>
                    <td class="px-4 py-3 text-end text-muted small">
                      {{ new Date(scoreEntry.date).toLocaleDateString('fr-FR') }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero-section {
  padding: 3rem 0;
}

.card {
  border-radius: 15px;
  overflow: hidden;
}

.score-row {
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.score-row:hover {
  background-color: #f8f9fa;
  border-left-color: #667eea;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  background-color: #e9ecef;
  color: #495057;
}

.rank-gold {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  color: #856404;
}

.rank-silver {
  background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
  color: #383d41;
}

.rank-bronze {
  background: linear-gradient(135deg, #cd7f32 0%, #daa06d 100%);
  color: #fff;
}

.score-value {
  font-weight: 600;
  color: #667eea;
}

.btn-light:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
}

.color-drops {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.color-drops::before,
.color-drops::after {
  content: '';
  position: absolute;
  top: -10%;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  animation: fall 3s linear infinite;
}

.color-drops::before {
  background: red;
  left: 25%;
  animation-delay: 0s;
}

.color-drops::after {
  background: limegreen;
  left: 60%;
  animation-delay: 2s;
}

@keyframes fall {
  0% {
    transform: translateY(-10%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translateY(110vh) scale(0.8);
    opacity: 0;
  }
}

.color-drops span {
  position: absolute;
  top: -10%;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: fall 6s linear infinite;
}

.color-drops span:nth-child(1) {
  left: 10%;
  background: #ff006e;
  animation-delay: 1s;
}

.color-drops span:nth-child(2) {
  left: 40%;
  background: #00ff88;
  animation-delay: 2.5s;
}

.color-drops span:nth-child(3) {
  left: 70%;
  background: #00b4d8;
  animation-delay: 3.2s;
}

.color-drops span:nth-child(4) {
  left: 85%;
  background: #ffbe0b;
  animation-delay: 4s;
}
</style>
