<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';

const registeredScores = ref([]);
const totalQuestions = ref(0);

onMounted(async () => {
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
  <div class="page-wrapper">
    <div class="container-fluid px-4 py-5">
      <div class="main-grid">
        <div class="hero-card contner">
          <div class="contner-inner">
            <div class="hero-content">
              <img src="@/assets/logoZy.png" alt="ZyraQ Logo" class="hero-logo">
              <p class="hero-description text-white-50 mb-5">
                Teste tes connaissances avec <span class="highlight">{{ totalQuestions }} questions</span> passionnantes
              </p>
              <router-link to="/new-quiz" class="btn btn-gradient btn-lg px-5 py-3 shadow">
                Démarrer le Quiz
              </router-link>
              
              <div class="stats-mini mt-5">
                <div class="stat-item">
                  <div class="stat-number">{{ registeredScores.length }}</div>
                  <div class="stat-label">Participants</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ totalQuestions }}</div>
                  <div class="stat-label">Questions</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="scores-card contner">
          <div class="contner-inner">
            <div class="scores-content">
              <div class="scores-header mb-4">
                <h2 class="scores-title text-white">
                  Tableau des Scores
                </h2>
              </div>
              
              <div v-if="registeredScores.length === 0" class="empty-scores text-center py-5">
                <p class="text-white-50 mb-0">Pas encore de scores.<br>Sois le premier à jouer !</p>
              </div>
              
              <div v-else class="scores-list">
                <div
                  v-for="(scoreEntry, index) in registeredScores"
                  :key="scoreEntry.date"
                  class="score-item"
                  :class="getRankClass(index)"
                >
                  <div class="score-rank">
                    <span class="rank-number">{{ index + 1 }}</span>
                  </div>
                  <div class="score-info">
                    <div class="player-name">{{ scoreEntry.playerName }}</div>
                    <div class="score-date">{{ new Date(scoreEntry.date).toLocaleDateString('fr-FR') }}</div>
                  </div>
                  <div class="score-points">
                    <span class="points">{{ scoreEntry.score }}</span>
                    <span class="separator">/</span>
                    <span class="total">{{ totalQuestions }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-wrapper {
  position: relative;
  min-height: calc(100vh - 200px);
}

.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  align-items: start;
}

@media (max-width: 992px) {
  .main-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}

.contner {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  padding: 4px;
  border-radius: 30px;
  z-index: 1;
  height: 100%;
}

.contner-inner {
  background-color: #090043;
  padding: 3rem;
  border-radius: 26px;
  width: 100%;
  height: 100%;
}

.hero-card {
  min-height: 600px;
  display: flex;
  flex-direction: column;
}

.hero-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  height: 100%;
  justify-content: center;
}

.hero-logo {
  max-width: 350px;
  height: auto;
  filter: drop-shadow(0 0 30px rgba(240, 189, 30, 0.6));
}

.hero-icon {
  color: #f0bd1e;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  letter-spacing: 2px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 1.3rem;
  line-height: 1.6;
}

.highlight {
  color: #f0bd1e;
  font-weight: 700;
  font-size: 1.4rem;
}

.stats-mini {
  display: flex;
  gap: 3rem;
  margin-top: 3rem;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.scores-card {
  min-height: 600px;
}

.scores-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.scores-header {
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 1rem;
}

.scores-title {
  font-size: 1.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-scores {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.5);
}

.scores-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 500px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.scores-list::-webkit-scrollbar {
  width: 6px;
}

.scores-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.scores-list::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 10px;
}

.score-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.score-item:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #f0bd1e;
  transform: translateX(5px);
}

.score-item.rank-gold {
  border-color: rgba(255, 215, 0, 0.5);
  background: rgba(255, 215, 0, 0.1);
}

.score-item.rank-silver {
  border-color: rgba(192, 192, 192, 0.5);
  background: rgba(192, 192, 192, 0.1);
}

.score-item.rank-bronze {
  border-color: rgba(205, 127, 50, 0.5);
  background: rgba(205, 127, 50, 0.1);
}

.score-rank {
  flex-shrink: 0;
}

.rank-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  color: white;
  font-weight: 800;
  font-size: 1.2rem;
  border-radius: 12px;
}

.rank-gold .rank-number {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: #856404;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}

.rank-silver .rank-number {
  background: linear-gradient(135deg, #c0c0c0, #e8e8e8);
  color: #383d41;
  box-shadow: 0 0 20px rgba(192, 192, 192, 0.5);
}

.rank-bronze .rank-number {
  background: linear-gradient(135deg, #cd7f32, #daa06d);
  color: white;
  box-shadow: 0 0 20px rgba(205, 127, 50, 0.5);
}

.score-info {
  flex: 1;
}

.player-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: white;
  margin-bottom: 0.25rem;
}

.score-date {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.5);
}

.score-points {
  display: flex;
  align-items: baseline;
  gap: 0.3rem;
  font-weight: 700;
  flex-shrink: 0;
}

.points {
  font-size: 1.8rem;
  color: #f0bd1e;
}

.separator {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.4);
}

.total {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.6);
}

.btn-gradient {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border: none;
  color: white;
  font-weight: 700;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-gradient:hover {
  background: linear-gradient(135deg, #cc13b5, #f0bd1e);
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(240, 189, 30, 0.4) !important;
  color: white;
}
</style>
