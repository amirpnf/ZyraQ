<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import quizApiService from '@/services/QuizApiService';
import adminAuthService from '@/services/AdminAuthService';

const router = useRouter();
const password = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

onMounted(() => {
  if (adminAuthService.isAdminLoggedIn()) {
    router.push('/admin/questions');
  }
});

async function handleLogin() {
  if (!password.value.trim()) {
    errorMessage.value = 'Entre le mot de passe';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const response = await quizApiService.login(password.value);

    if (response.status === 200 && response.data.token) {
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
  <div class="container mt-5 mb-5 pb-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="admin-container">
          <div class="admin-container-inner">
            <div class="admin-header text-center py-4">
              <h2 class="h3 mb-0 text-white">Administration</h2>
            </div>
            <div class="admin-body p-5">
              <div class="text-center mb-4">
                <p class="text-white-50">Connecte-toi pour gérer les questions</p>
              </div>

              <form @submit.prevent="handleLogin">
                <div class="mb-4">
                  <label for="password" class="form-label fw-semibold text-white">
                    Mot de passe
                  </label>
                  <input
                    id="password"
                    type="password"
                    class="form-control form-control-lg custom-input"
                    v-model="password"
                    placeholder="Mot de passe administrateur"
                    @keyup.enter="handleLogin"
                    :disabled="isLoading"
                  />
                </div>

                <div v-if="errorMessage" class="alert alert-danger-custom border-0" role="alert">
                  {{ errorMessage }}
                </div>

                <div class="d-grid gap-3">
                  <button type="submit" class="btn btn-gradient btn-lg" :disabled="isLoading">
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
                  <router-link to="/" class="btn btn-outline-light"> Retour </router-link>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div class="alert alert-custom border-0 shadow-sm mt-4" role="alert">
          <strong>Accès admin :</strong> Zone réservée
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
  background: linear-gradient(90deg, #f0bd1e, #cc13b5);
  padding: 9px;
  border-radius: 39px;
}

.admin-container-inner {
  background-color: #090043;
  border-radius: 30px;
  width: 100%;
  height: 100%;
}

.btn-gradient {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
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

.alert-custom {
  background: linear-gradient(90deg, #f0bd1e, #cc13b5);
  color: white;
  border-radius: 15px;
}

.alert-danger-custom {
  background: linear-gradient(135deg, #ff006e, #d00000);
  color: white;
  border-radius: 15px;
}
</style>
