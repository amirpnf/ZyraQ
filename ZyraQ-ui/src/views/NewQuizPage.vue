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
  
  participationStorageService.clear();
  participationStorageService.savePlayerName(username.value);
  
  router.push('/questions');
}
</script>

<template>
  <div class="page-wrapper">
    <div class="container-fluid px-4 py-5">
      <div class="new-quiz-layout">
        <div class="motivation-card contner">
          <div class="contner-inner">
            <div class="motivation-content">
              <h2 class="motivation-title text-white mb-3">Prêt pour le défi ?</h2>
              <p class="motivation-text text-white-50 mb-4">
                Tu es sur le point de tester tes connaissances. Prends ton temps, réfléchis bien, et surtout... amuse-toi !
              </p>
            </div>
          </div>
        </div>

        <div class="form-card contner">
          <div class="contner-inner">
            <div class="form-content">
              <div class="form-header text-center mb-5">
                <h1 class="form-title text-white mb-2">Nouvelle Participation</h1>
                <p class="form-subtitle text-white-50">Entre ton nom pour commencer l'aventure</p>
              </div>

              <div class="input-group-custom mb-4">
                <label for="playerName" class="input-label text-white">
                  Nom du participant
                </label>
                <input
                  id="playerName"
                  type="text"
                  class="custom-input"
                  v-model="username"
                  placeholder="Entre ton nom..."
                  @keyup.enter="launchNewQuiz"
                  autofocus
                />
                <small class="input-hint text-white-50">
                  Ton nom apparaîtra dans le classement
                </small>
              </div>

              <div class="buttons-wrapper">
                <button
                  type="button"
                  class="btn btn-gradient btn-lg w-100 mb-3"
                  @click="launchNewQuiz"
                >
                  Commencer le Quiz
                </button>
                <router-link to="/" class="btn btn-outline-light w-100">
                  Retour à l'accueil
                </router-link>
              </div>

              <div class="info-box mt-4">
                <span class="text-white-50 small">Prends ton temps pour chaque question</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-wrapper {
  min-height: calc(100vh - 200px);
  position: relative;
}

.new-quiz-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2.5rem;
  max-width: 1400px;
  margin: 0 auto;
  align-items: center;
}

@media (max-width: 992px) {
  .new-quiz-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}

.contner {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  padding: 4px;
  border-radius: 30px;
  z-index: 1;
}

.contner-inner {
  background-color: #090043;
  padding: 3rem;
  border-radius: 26px;
  width: 100%;
  height: 100%;
}

.motivation-card {
  min-height: 500px;
  display: flex;
  align-items: center;
}

.motivation-content {
  text-align: center;
}

.icon-group {
  color: #f0bd1e;
}

.motivation-title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.motivation-text {
  font-size: 1.15rem;
  line-height: 1.6;
}

.form-card {
  min-height: 500px;
  display: flex;
  align-items: center;
}

.form-content {
  width: 100%;
}

.form-title {
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.form-subtitle {
  font-size: 1rem;
}

.input-group-custom {
  margin-bottom: 2rem;
}

.input-label {
  display: flex;
  align-items: center;
  font-weight: 600;
  margin-bottom: 0.75rem;
  font-size: 1.05rem;
}

.custom-input {
  width: 100%;
  padding: 1.25rem 1.5rem;
  font-size: 1.1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 14px;
  color: white;
  transition: all 0.3s ease;
}

.custom-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.custom-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.12);
  border-color: #f0bd1e;
  box-shadow: 0 0 0 4px rgba(240, 189, 30, 0.15);
}

.input-hint {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.buttons-wrapper {
  margin-top: 2rem;
}

.btn-gradient {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border: none;
  color: white;
  font-weight: 700;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-gradient:hover {
  background: linear-gradient(135deg, #cc13b5, #f0bd1e);
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(240, 189, 30, 0.4) !important;
  color: white;
}

.btn-outline-light {
  border: 2px solid rgba(255, 255, 255, 0.4);
  color: rgba(255, 255, 255, 0.8);
  background: transparent;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  font-weight: 600;
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
  color: white;
  transform: translateY(-2px);
}

.info-box {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(240, 189, 30, 0.1);
  border: 1px solid rgba(240, 189, 30, 0.3);
  border-radius: 12px;
}

@media (max-width: 768px) {
  .contner-inner {
    padding: 2rem;
  }
  
  .motivation-title,
  .form-title {
    font-size: 1.8rem;
  }
  
  .custom-input {
    font-size: 1rem;
    padding: 1rem;
  }
}
</style>
