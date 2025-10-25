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
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-lg border-0">
          <div class="card-header bg-white border-0 py-4">
            <h2 class="h3 mb-0 text-center text-dark">Nouvelle Participation</h2>
          </div>
          <div class="card-body p-5">
            <div class="mb-4 text-center">
              <p class="text-muted">
                Entre ton nom pour commencer
              </p>
            </div>

            <div class="mb-4">
              <label for="playerName" class="form-label fw-semibold">
                Nom du participant
              </label>
              <input
                id="playerName"
                type="text"
                class="form-control form-control-lg"
                v-model="username"
                placeholder="Votre nom"
                @keyup.enter="launchNewQuiz"
              />
              <small class="form-text text-muted mt-2 d-block">
                Ton nom sera dans le classement
              </small>
            </div>

            <div class="d-grid gap-3">
              <button
                type="button"
                class="btn btn-primary btn-lg"
                @click="launchNewQuiz"
              >
                Commencer le Quiz
              </button>
              <router-link to="/" class="btn btn-outline-secondary">
                Retour
              </router-link>
            </div>
          </div>
        </div>

        <div class="alert alert-info border-0 shadow-sm mt-4" role="alert">
          <strong>Info :</strong> Prends ton temps pour chaque question
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  border-radius: 15px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.25rem rgba(102, 126, 234, 0.25);
}
</style>
