<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import quizApiService from '@/services/QuizApiService';
import adminAuthService from '@/services/AdminAuthService';

const router = useRouter();
const route = useRoute();
const token = ref('');
const isLoading = ref(false);
const isEditMode = ref(false);
const questionId = ref(null);

const formData = ref({
  title: '',
  text: '',
  position: 1,
  image: '',
  difficulty: 'easy',
  possibleAnswers: [
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
  ],
});

onMounted(async () => {
  token.value = adminAuthService.getToken();
  if (!token.value) {
    router.push('/admin/login');
    return;
  }

  if (route.params.id) {
    isEditMode.value = true;
    questionId.value = parseInt(route.params.id);
    await loadQuestion();
  }
});

async function loadQuestion() {
  isLoading.value = true;
  try {
    const response = await quizApiService.getQuestionById(
      questionId.value,
      token.value
    );
    if (response && response.data) {
      const q = response.data;
      formData.value = {
        title: q.title || '',
        text: q.text || '',
        position: q.position || 1,
        image: q.image || '',
        difficulty: q.difficulty || 'easy',
        possibleAnswers: q.possibleAnswers || [
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
        ],
      };
    }
  } catch (error) {
    console.error('Erreur chargement question:', error);
    alert('Erreur chargement');
  } finally {
    isLoading.value = false;
  }
}

function addAnswer() {
  formData.value.possibleAnswers.push({ text: '', isCorrect: false });
}

function removeAnswer(index) {
  if (formData.value.possibleAnswers.length > 2) {
    formData.value.possibleAnswers.splice(index, 1);
  } else {
    alert('Minimum 2 réponses');
  }
}

async function handleSubmit() {
  // Validation
  if (!formData.value.title.trim()) {
    alert('Le titre est obligatoire');
    return;
  }

  const validAnswers = formData.value.possibleAnswers.filter((a) =>
    a.text.trim()
  );
  if (validAnswers.length < 2) {
    alert('Minimum 2 réponses');
    return;
  }

  const correctAnswers = validAnswers.filter((a) => a.isCorrect);
  if (correctAnswers.length === 0) {
    alert('Au moins 1 réponse correcte');
    return;
  }

  isLoading.value = true;
  try {
    const payload = {
      ...formData.value,
      possibleAnswers: validAnswers,
    };

    if (isEditMode.value) {
      await quizApiService.updateQuestion(
        questionId.value,
        payload,
        token.value
      );
      alert('Question modifiée');
    } else {
      await quizApiService.createQuestion(payload, token.value);
      alert('Question créée');
    }

    router.push('/admin/questions');
  } catch (error) {
    console.error('Erreur sauvegarde:', error);
    alert('Erreur lors de la sauvegarde');
  } finally {
    isLoading.value = false;
  }
}

function cancel() {
  router.push('/admin/questions');
}
</script>

<template>
  <div>
    <div class="color-drops">
      <span v-for="n in 40" :key="n"></span>
    </div>
    <div class="container mt-4 mb-5 pb-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="form-container">
            <div class="form-container-inner">
              <div class="form-header py-4">
                <h2 class="h4 mb-0 text-white text-center">
                  {{ isEditMode ? 'Modifier la question' : 'Créer une question' }}
                </h2>
              </div>
              <div class="form-body p-4">
                <form @submit.prevent="handleSubmit">
                  <div class="row">
                    <div class="col-md-8 mb-3">
                      <label for="title" class="form-label fw-semibold text-white">
                        Titre
                      </label>
                      <input
                        id="title"
                        type="text"
                        class="form-control custom-input"
                        v-model="formData.title"
                        placeholder="Ex: Quelle est la capitale de la France ?"
                        required
                      />
                    </div>
                    <div class="col-md-2 mb-3">
                      <label for="position" class="form-label fw-semibold text-white">
                        Position
                      </label>
                      <input
                        id="position"
                        type="number"
                        class="form-control custom-input"
                        v-model.number="formData.position"
                        min="1"
                        required
                      />
                    </div>
                    <div class="col-md-2 mb-3">
                      <label for="difficulty" class="form-label fw-semibold text-white">
                        Difficulté
                      </label>
                      <select
                        id="difficulty"
                        class="form-select custom-select"
                        v-model="formData.difficulty"
                      >
                        <option value="easy">Facile</option>
                        <option value="medium">Moyen</option>
                        <option value="hard">Difficile</option>
                      </select>
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="text" class="form-label fw-semibold text-white">
                      Description
                    </label>
                    <textarea
                      id="text"
                      class="form-control custom-input"
                      v-model="formData.text"
                      rows="3"
                      placeholder="Description additionnelle (optionnel)"
                    ></textarea>
                  </div>

                  <div class="mb-4">
                    <label for="image" class="form-label fw-semibold text-white">
                      Image (Base64 ou URL)
                    </label>
                    <textarea
                      id="image"
                      class="form-control custom-input"
                      v-model="formData.image"
                      rows="2"
                      placeholder="data:image/png;base64,... ou URL de l'image"
                    ></textarea>
                    <small class="text-white-50">
                      Laisse vide si pas d'image
                    </small>
                  </div>

                  <div class="mb-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                      <h5 class="mb-0 text-white">Réponses possibles</h5>
                      <button
                        type="button"
                        @click="addAnswer"
                        class="btn btn-sm btn-outline-light"
                      >
                        Ajouter une réponse
                      </button>
                    </div>

                    <div
                      v-for="(answer, index) in formData.possibleAnswers"
                      :key="index"
                      class="answer-card mb-2"
                    >
                      <div class="row align-items-center g-3">
                        <div class="col-auto">
                          <span class="answer-letter-badge">
                            {{ String.fromCharCode(65 + index) }}
                          </span>
                        </div>
                        <div class="col">
                          <input
                            type="text"
                            class="form-control custom-input"
                            v-model="answer.text"
                            :placeholder="`Réponse ${String.fromCharCode(65 + index)}`"
                          />
                        </div>
                        <div class="col-auto">
                          <div class="form-check">
                            <input
                              type="checkbox"
                              class="form-check-input custom-checkbox"
                              :id="`correct-${index}`"
                              v-model="answer.isCorrect"
                            />
                            <label
                              class="form-check-label text-white"
                              :for="`correct-${index}`"
                            >
                              Correcte
                            </label>
                          </div>
                        </div>
                        <div class="col-auto">
                          <button
                            type="button"
                            @click="removeAnswer(index)"
                            class="btn btn-sm btn-outline-danger"
                            :disabled="formData.possibleAnswers.length <= 2"
                          >
                            Supprimer
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="d-flex gap-2">
                    <button
                      type="submit"
                      class="btn btn-gradient px-4"
                      :disabled="isLoading"
                    >
                      <span v-if="isLoading">
                        <span
                          class="spinner-border spinner-border-sm me-2"
                          role="status"
                        ></span>
                        Sauvegarde...
                      </span>
                      <span v-else>
                        {{ isEditMode ? 'Modifier' : 'Créer' }}
                      </span>
                    </button>
                    <button
                      type="button"
                      @click="cancel"
                      class="btn btn-outline-light px-4"
                      :disabled="isLoading"
                    >
                      Annuler
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.color-drops {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  z-index: -1;
  opacity: 0.4;
}

.color-drops span {
  position: absolute;
  top: -100%;
  width: 8px;
  height: 200px;
  background: linear-gradient(45deg, #f0bd1e, #cc13b5);
  border-radius: 50px;
  animation: drop linear infinite;
}

.color-drops span:nth-child(1) { left: 2%; animation-duration: 8s; animation-delay: 0s; }
.color-drops span:nth-child(2) { left: 5%; animation-duration: 12s; animation-delay: 1s; }
.color-drops span:nth-child(3) { left: 8%; animation-duration: 10s; animation-delay: 0.5s; }
.color-drops span:nth-child(4) { left: 12%; animation-duration: 14s; animation-delay: 2s; }
.color-drops span:nth-child(5) { left: 15%; animation-duration: 9s; animation-delay: 0.8s; }
.color-drops span:nth-child(6) { left: 18%; animation-duration: 11s; animation-delay: 1.5s; }
.color-drops span:nth-child(7) { left: 22%; animation-duration: 13s; animation-delay: 0.3s; }
.color-drops span:nth-child(8) { left: 25%; animation-duration: 7s; animation-delay: 1.8s; }
.color-drops span:nth-child(9) { left: 28%; animation-duration: 15s; animation-delay: 0.7s; }
.color-drops span:nth-child(10) { left: 32%; animation-duration: 8s; animation-delay: 2.2s; }
.color-drops span:nth-child(11) { left: 35%; animation-duration: 12s; animation-delay: 1.2s; }
.color-drops span:nth-child(12) { left: 38%; animation-duration: 10s; animation-delay: 0.9s; }
.color-drops span:nth-child(13) { left: 42%; animation-duration: 14s; animation-delay: 1.7s; }
.color-drops span:nth-child(14) { left: 45%; animation-duration: 9s; animation-delay: 0.4s; }
.color-drops span:nth-child(15) { left: 48%; animation-duration: 11s; animation-delay: 2.1s; }
.color-drops span:nth-child(16) { left: 52%; animation-duration: 13s; animation-delay: 0.6s; }
.color-drops span:nth-child(17) { left: 55%; animation-duration: 7s; animation-delay: 1.9s; }
.color-drops span:nth-child(18) { left: 58%; animation-duration: 15s; animation-delay: 1.1s; }
.color-drops span:nth-child(19) { left: 62%; animation-duration: 8s; animation-delay: 0.2s; }
.color-drops span:nth-child(20) { left: 65%; animation-duration: 12s; animation-delay: 1.6s; }
.color-drops span:nth-child(21) { left: 68%; animation-duration: 10s; animation-delay: 0.1s; }
.color-drops span:nth-child(22) { left: 72%; animation-duration: 14s; animation-delay: 2.3s; }
.color-drops span:nth-child(23) { left: 75%; animation-duration: 9s; animation-delay: 1.3s; }
.color-drops span:nth-child(24) { left: 78%; animation-duration: 11s; animation-delay: 0.5s; }
.color-drops span:nth-child(25) { left: 82%; animation-duration: 13s; animation-delay: 2s; }
.color-drops span:nth-child(26) { left: 85%; animation-duration: 7s; animation-delay: 0.8s; }
.color-drops span:nth-child(27) { left: 88%; animation-duration: 15s; animation-delay: 1.4s; }
.color-drops span:nth-child(28) { left: 92%; animation-duration: 8s; animation-delay: 0.7s; }
.color-drops span:nth-child(29) { left: 95%; animation-duration: 12s; animation-delay: 2.4s; }
.color-drops span:nth-child(30) { left: 98%; animation-duration: 10s; animation-delay: 1s; }
.color-drops span:nth-child(31) { left: 3%; animation-duration: 14s; animation-delay: 1.8s; }
.color-drops span:nth-child(32) { left: 7%; animation-duration: 9s; animation-delay: 0.3s; }
.color-drops span:nth-child(33) { left: 11%; animation-duration: 11s; animation-delay: 2.1s; }
.color-drops span:nth-child(34) { left: 14%; animation-duration: 13s; animation-delay: 0.6s; }
.color-drops span:nth-child(35) { left: 17%; animation-duration: 7s; animation-delay: 1.7s; }
.color-drops span:nth-child(36) { left: 21%; animation-duration: 15s; animation-delay: 0.9s; }
.color-drops span:nth-child(37) { left: 24%; animation-duration: 8s; animation-delay: 2.2s; }
.color-drops span:nth-child(38) { left: 27%; animation-duration: 12s; animation-delay: 1.1s; }
.color-drops span:nth-child(39) { left: 31%; animation-duration: 10s; animation-delay: 0.4s; }
.color-drops span:nth-child(40) { left: 34%; animation-duration: 14s; animation-delay: 1.9s; }

@keyframes drop {
  to {
    transform: translateY(calc(100vh + 200px));
  }
}

.form-container {
  padding: 4px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.form-container-inner {
  background: #090043;
  border-radius: 12px;
  overflow: hidden;
}

.form-header {
  background: linear-gradient(135deg, rgba(240, 189, 30, 0.1), rgba(204, 19, 181, 0.1));
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.form-body {
  background: #090043;
}

.custom-input {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: white;
  padding: 12px 16px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.custom-input:focus {
  background: rgba(255, 255, 255, 0.15);
  border-color: #f0bd1e;
  box-shadow: 0 0 0 0.25rem rgba(240, 189, 30, 0.25);
  color: white;
}

.custom-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.custom-select {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: white;
  padding: 12px 16px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.custom-select:focus {
  background: rgba(255, 255, 255, 0.15);
  border-color: #f0bd1e;
  box-shadow: 0 0 0 0.25rem rgba(240, 189, 30, 0.25);
  color: white;
}

.custom-select option {
  background: #090043;
  color: white;
}

.custom-checkbox {
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.custom-checkbox:checked {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-color: #f0bd1e;
}

.answer-card {
  background: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.answer-card:hover {
  border-color: rgba(240, 189, 30, 0.5);
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.answer-letter-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 1rem;
}

.btn-gradient {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border: none;
  color: white;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(240, 189, 30, 0.4);
  color: white;
}

.btn-outline-light {
  border: 2px solid rgba(255, 255, 255, 0.6);
  color: rgba(255, 255, 255, 0.8);
  background: #090043;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateY(-1px);
}

.btn-outline-danger {
  border: 2px solid #dc3545;
  color: #dc3545;
  background: #090043;
  transition: all 0.3s ease;
}

.btn-outline-danger:hover {
  background: #dc3545;
  color: white;
  transform: translateY(-1px);
}

.btn-outline-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-outline-danger:disabled:hover {
  transform: none;
  background: #090043;
  color: #dc3545;
}

@media (max-width: 768px) {
  .form-container {
    padding: 2px;
  }
  
  .custom-input, .custom-select {
    font-size: 14px;
    padding: 10px 14px;
  }
  
  .answer-card {
    padding: 0.75rem;
  }
  
  .answer-letter-badge {
    width: 32px;
    height: 32px;
    font-size: 0.9rem;
  }
}
</style>
