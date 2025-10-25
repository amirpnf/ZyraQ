<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';
import adminAuthService from '@/services/AdminAuthService';

const router = useRouter();
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

async function handleLogin() {
  if (!password.value.trim()) {
    errorMessage.value = 'Entre le mot de passe';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const response = await quizApiService.login(password.value);
    if (response && response.data && response.data.token) {
      adminAuthService.saveToken(response.data.token);
      router.push('/admin/questions');
    } else {
      errorMessage.value = 'Erreur connexion';
    }
  } catch (error) {
    errorMessage.value = 'Mauvais mot de passe';
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card shadow-lg border-0">
          <div class="card-header bg-white border-0 py-4">
            <h2 class="h3 mb-0 text-center text-dark">Administration</h2>
          </div>
          <div class="card-body p-5">
            <div class="text-center mb-4">
              <p class="text-muted">
                Connecte-toi pour gérer les questions
              </p>
            </div>

            <form @submit.prevent="handleLogin">
              <div class="mb-4">
                <label for="password" class="form-label fw-semibold">
                  Mot de passe
                </label>
                <input
                  id="password"
                  type="password"
                  class="form-control form-control-lg"
                  v-model="password"
                  placeholder="Mot de passe administrateur"
                  @keyup.enter="handleLogin"
                  :disabled="isLoading"
                />
              </div>

              <div v-if="errorMessage" class="alert alert-danger border-0" role="alert">
                {{ errorMessage }}
              </div>

              <div class="d-grid gap-3">
                <button
                  type="submit"
                  class="btn btn-dark btn-lg"
                  :disabled="isLoading"
                >
                  <span v-if="isLoading">
                    <span
                      class="spinner-border spinner-border-sm me-2"
                      role="status"
                      aria-hidden="true"
                    ></span>
                    Connexion...
                  </span>
                  <span v-else> Se connecter </span>
                </button>
                <router-link to="/" class="btn btn-outline-secondary">
                  Retour
                </router-link>
              </div>
            </form>
          </div>
        </div>

        <div class="alert alert-info border-0 shadow-sm mt-4" role="alert">
          <strong>Accès admin :</strong> Zone réservée
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  border: none;
  border-radius: 15px;
}

.card-header {
  border-radius: 15px 15px 0 0 !important;
}
</style>
