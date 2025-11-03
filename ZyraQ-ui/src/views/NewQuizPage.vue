<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';

const router = useRouter();
const username = ref('');

function launchNewQuiz() {
  if (username.value.trim() === '') {
    alert('Entre ton nom');
    return;
  }

  console.log('Launch quiz:', username.value);
  
  participationStorageService.clear();
  participationStorageService.savePlayerName(username.value);
  
  router.push('/questions');
}
</script>

<template>
  <div class="color-drops">
    <span v-for="n in 40" :key="n"></span>
  </div>
  <div class="container mt-5 mb-5 pb-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="quiz-container">
          <div class="quiz-container-inner">
            <div class="quiz-header text-center py-4">
              <h2 class="h3 mb-0 text-white">Nouvelle Participation</h2>
            </div>
            <div class="quiz-body p-5">
              <div class="mb-4 text-center">
                <p class="text-white-50">
                  Entre ton nom pour commencer
                </p>
              </div>

              <div class="mb-4">
                <label for="playerName" class="form-label fw-semibold text-white">
                  Nom du participant
                </label>
                <input
                  id="playerName"
                  type="text"
                  class="form-control form-control-lg custom-input"
                  v-model="username"
                  placeholder="Votre nom"
                  @keyup.enter="launchNewQuiz"
                />
                <small class="form-text text-white-50 mt-2 d-block">
                  Ton nom sera dans le classement
                </small>
              </div>

              <div class="d-grid gap-3">
                <button
                  type="button"
                  class="btn btn-gradient btn-lg"
                  @click="launchNewQuiz"
                >
                  Commencer le Quiz
                </button>
                <router-link to="/" class="btn btn-outline-light">
                  Retour
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <div class="alert alert-custom border-0 shadow-sm mt-4" role="alert">
          <strong>Info :</strong> Prends ton temps pour chaque question
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Animation des gouttes de couleur */
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

/* Conteneur principal avec bordure dégradée */
.quiz-container {
  background: linear-gradient(90deg, #f0bd1e, #cc13b5);
  padding: 9px;
  border-radius: 39px;
  z-index: 1;
}

.quiz-container-inner {
  background-color: #090043;
  border-radius: 30px;
  width: 100%;
  height: 100%;
}

/* Bouton avec dégradé */
.btn-gradient {
  background: linear-gradient(90deg, #f0bd1e, #cc13b5);
  border: none;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  background: linear-gradient(90deg, #cc13b5, #f0bd1e);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(204, 19, 181, 0.3) !important;
  color: white;
}

/* Input personnalisé */
.custom-input {
  background-color: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.custom-input:focus {
  background-color: rgba(255, 255, 255, 0.15);
  border-color: #f0bd1e;
  box-shadow: 0 0 0 0.25rem rgba(240, 189, 30, 0.25);
  color: white;
}

.custom-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.btn-outline-light {
  border: 2px solid rgba(255, 255, 255, 0.6);
  color: rgba(255, 255, 255, 0.8);
  background: #090043;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: white;
  color: white;
}

/* Alert personnalisée */
.alert-custom {
  background: linear-gradient(90deg, #f0bd1e, #cc13b5);
  color: white;
  border-radius: 15px;
}
</style>
