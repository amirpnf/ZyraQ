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
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <div class="card shadow-lg border-0">
          <div class="card-header bg-white border-0 py-4">
            <h2 class="h4 mb-0 text-dark">
              {{ isEditMode ? 'Modifier la question' : 'Créer une question' }}
            </h2>
          </div>
          <div class="card-body p-4">
            <form @submit.prevent="handleSubmit">
              <div class="row">
                <div class="col-md-8 mb-3">
                  <label for="title" class="form-label fw-semibold">
                    Titre
                  </label>
                  <input
                    id="title"
                    type="text"
                    class="form-control"
                    v-model="formData.title"
                    placeholder="Ex: Quelle est la capitale de la France ?"
                    required
                  />
                </div>
                <div class="col-md-2 mb-3">
                  <label for="position" class="form-label fw-semibold">
                    Position
                  </label>
                  <input
                    id="position"
                    type="number"
                    class="form-control"
                    v-model.number="formData.position"
                    min="1"
                    required
                  />
                </div>
                <div class="col-md-2 mb-3">
                  <label for="difficulty" class="form-label fw-semibold">
                    Difficulté
                  </label>
                  <select
                    id="difficulty"
                    class="form-select"
                    v-model="formData.difficulty"
                  >
                    <option value="easy">Facile</option>
                    <option value="medium">Moyen</option>
                    <option value="hard">Difficile</option>
                  </select>
                </div>
              </div>

              <div class="mb-3">
                <label for="text" class="form-label fw-semibold">
                  Description
                </label>
                <textarea
                  id="text"
                  class="form-control"
                  v-model="formData.text"
                  rows="3"
                  placeholder="Description additionnelle (optionnel)"
                ></textarea>
              </div>

              <div class="mb-4">
                <label for="image" class="form-label fw-semibold">
                  Image (Base64 ou URL)
                </label>
                <textarea
                  id="image"
                  class="form-control"
                  v-model="formData.image"
                  rows="2"
                  placeholder="data:image/png;base64,... ou URL de l'image"
                ></textarea>
                <small class="text-muted">
                  Laisse vide si pas d'image
                </small>
              </div>

              <div class="mb-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="mb-0">Réponses possibles</h5>
                  <button
                    type="button"
                    @click="addAnswer"
                    class="btn btn-sm btn-outline-dark"
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
                        class="form-control"
                        v-model="answer.text"
                        :placeholder="`Réponse ${String.fromCharCode(65 + index)}`"
                      />
                    </div>
                    <div class="col-auto">
                      <div class="form-check">
                        <input
                          type="checkbox"
                          class="form-check-input"
                          :id="`correct-${index}`"
                          v-model="answer.isCorrect"
                        />
                        <label
                          class="form-check-label"
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
                  class="btn btn-dark px-4"
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
                  class="btn btn-outline-secondary px-4"
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
</template>

<style scoped>
.card {
  border-radius: 15px;
}

.answer-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 10px;
  border: 2px solid #e9ecef;
  transition: all 0.2s;
}

.answer-card:hover {
  border-color: #667eea;
  background: white;
}

.answer-letter-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
}

.btn-dark {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  border: none;
}

.btn-dark:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(45, 55, 72, 0.4);
}
</style>
