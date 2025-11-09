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
const imagePreview = ref('');

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

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  if (!file.type.startsWith('image/')) {
    alert('Seulement les images sont autorisées');
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    formData.value.image = e.target.result;
    imagePreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
}

function removeImage() {
  formData.value.image = '';
  imagePreview.value = '';
}

async function handleSubmit() {
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
  <div class="page-wrapper">
    <div class="container-fluid px-4 py-4">
      <div class="form-top-bar mb-4">
        <div class="top-bar-inner">
          <h1 class="form-main-title">
            {{ isEditMode ? 'Modifier la question' : 'Créer une question' }}
          </h1>
          <div class="top-actions">
            <button
              type="button"
              @click="cancel"
              class="btn-cancel"
              :disabled="isLoading"
            >
              Annuler
            </button>
            <button
              @click="handleSubmit"
              class="btn-save"
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
                {{ isEditMode ? 'Enregistrer' : 'Créer la question' }}
              </span>
            </button>
          </div>
        </div>
      </div>

      <div class="form-layout">
        <div class="form-left">
          <div class="info-card contner">
            <div class="contner-inner">
              <h3 class="section-title text-white mb-4">Informations</h3>
              
              <div class="mb-4">
                <label for="title" class="input-label text-white">
                  Titre de la question
                </label>
                <input
                  id="title"
                  type="text"
                  class="custom-input"
                  v-model="formData.title"
                  placeholder="Ex: Quelle est la capitale de la France ?"
                  required
                />
              </div>

              <div class="mb-4">
                <label for="text" class="input-label text-white">
                  Description
                </label>
                <textarea
                  id="text"
                  class="custom-input"
                  v-model="formData.text"
                  rows="4"
                  placeholder="Description additionnelle (optionnel)"
                ></textarea>
              </div>

              <div class="row g-3 mb-4">
                <div class="col-md-4">
                  <label for="position" class="input-label text-white">
                    Position
                  </label>
                  <input
                    id="position"
                    type="number"
                    class="custom-input"
                    v-model.number="formData.position"
                    min="1"
                    required
                  />
                </div>
                <div class="col-md-8">
                  <label for="difficulty" class="input-label text-white">
                    Difficulté
                  </label>
                  <select
                    id="difficulty"
                    class="custom-select"
                    v-model="formData.difficulty"
                  >
                    <option value="easy">Facile</option>
                    <option value="medium">Moyen</option>
                    <option value="hard">Difficile</option>
                  </select>
                </div>
              </div>

              <div class="mb-0">
                <label class="input-label text-white mb-3">
                  Image
                </label>
                
                <div v-if="imagePreview" class="image-preview-container mb-3">
                  <img :src="imagePreview" alt="Aperçu" class="image-preview" />
                  <button
                    type="button"
                    @click="removeImage"
                    class="btn-remove-image"
                  >
                    ✕ Supprimer
                  </button>
                </div>

                <label for="imageUpload" class="btn-upload-image">
                  <input
                    id="imageUpload"
                  type="file"
                  accept="image/*"
                  @change="handleImageUpload"
                  style="display: none;"
                />
                  Choisir une image
                </label>
                
                <small class="text-white-50 d-block mt-2">
                  Formats acceptés : JPG, PNG, GIF
                </small>
              </div>
            </div>
          </div>
        </div>

        <div class="form-right">
          <div class="answers-card contner">
            <div class="contner-inner">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h3 class="section-title text-white mb-0">Réponses</h3>
                <button
                  type="button"
                  @click="addAnswer"
                  class="btn-add-answer"
                >
                  + Ajouter
                </button>
              </div>

              <div class="answers-list">
                <div
                  v-for="(answer, index) in formData.possibleAnswers"
                  :key="index"
                  class="answer-item"
                >
                  <div class="answer-header">
                    <div class="answer-letter">
                      {{ String.fromCharCode(65 + index) }}
                    </div>
                    <div class="answer-controls">
                      <label class="checkbox-wrapper">
                        <input
                          type="checkbox"
                          class="custom-checkbox"
                          v-model="answer.isCorrect"
                        />
                        <span class="checkbox-label text-white">Correcte</span>
                      </label>
                      <button
                        type="button"
                        @click="removeAnswer(index)"
                        class="btn-remove"
                        :disabled="formData.possibleAnswers.length <= 2"
                        title="Supprimer"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                  <input
                    type="text"
                    class="answer-input"
                    v-model="answer.text"
                    :placeholder="`Réponse ${String.fromCharCode(65 + index)}`"
                  />
                </div>
              </div>

              <div class="answers-hint">
                <small class="text-white-50">
                  Minimum 2 réponses. Au moins 1 doit être correcte.
                </small>
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
  min-height: 100vh;
  position: relative;
  background: #090043;
}

.contner {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  padding: 3px;
  border-radius: 20px;
  position: relative;
  z-index: 1;
}

.contner-inner {
  background-color: #090043;
  padding: 2rem;
  border-radius: 17px;
  width: 100%;
  height: 100%;
}

.form-top-bar {
  position: relative;
  z-index: 1;
}

.top-bar-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, rgba(240, 189, 30, 0.15), rgba(204, 19, 181, 0.15));
  backdrop-filter: blur(10px);
  padding: 1.5rem 2rem;
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.form-main-title {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.top-actions {
  display: flex;
  gap: 1rem;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-cancel:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
  border-color: white;
  transform: translateY(-2px);
}

.btn-save {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(240, 189, 30, 0.4);
}

.btn-save:disabled,
.btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
  position: relative;
  z-index: 1;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
}

.input-label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.custom-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.08);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  padding: 1rem 1.25rem;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.custom-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.12);
  border-color: #f0bd1e;
  box-shadow: 0 0 0 4px rgba(240, 189, 30, 0.15);
}

.custom-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.custom-select {
  width: 100%;
  background: rgba(255, 255, 255, 0.08);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  padding: 1rem 1.25rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.custom-select:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.12);
  border-color: #f0bd1e;
  box-shadow: 0 0 0 4px rgba(240, 189, 30, 0.15);
}

.custom-select option {
  background: #090043;
  color: white;
}

.btn-add-answer {
  background: rgba(240, 189, 30, 0.15);
  border: 2px solid rgba(240, 189, 30, 0.4);
  color: #f0bd1e;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-add-answer:hover {
  background: rgba(240, 189, 30, 0.25);
  border-color: #f0bd1e;
  transform: translateY(-2px);
}

.answers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.answer-item {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  padding: 1rem;
  transition: all 0.3s ease;
}

.answer-item:hover {
  border-color: rgba(240, 189, 30, 0.4);
  background: rgba(255, 255, 255, 0.08);
}

.answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.answer-letter {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-radius: 50%;
  font-weight: 800;
  font-size: 1.1rem;
  color: white;
}

.answer-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.custom-checkbox {
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  cursor: pointer;
  appearance: none;
  position: relative;
  transition: all 0.3s ease;
}

.custom-checkbox:checked {
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  border-color: #f0bd1e;
}

.custom-checkbox:checked::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.checkbox-label {
  font-weight: 600;
  font-size: 0.9rem;
}

.btn-upload-image {
  display: inline-block;
  background: linear-gradient(135deg, #f0bd1e, #cc13b5);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.btn-upload-image:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(240, 189, 30, 0.4);
}

.image-preview-container {
  position: relative;
  display: inline-block;
  max-width: 100%;
}

.image-preview {
  max-width: 100%;
  max-height: 300px;
  border-radius: 12px;
  border: 3px solid rgba(240, 189, 30, 0.5);
  display: block;
}

.btn-remove-image {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(220, 53, 69, 0.9);
  border: 2px solid #dc3545;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-remove-image:hover {
  background: #dc3545;
  transform: scale(1.05);
}

.btn-remove {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(220, 53, 69, 0.1);
  border: 2px solid rgba(220, 53, 69, 0.3);
  color: #dc3545;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-remove:hover:not(:disabled) {
  background: #dc3545;
  border-color: #dc3545;
  color: white;
  transform: scale(1.1);
}

.btn-remove:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.answer-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.08);
  border: 2px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  color: white;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.answer-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.12);
  border-color: #f0bd1e;
}

.answer-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.answers-hint {
  padding: 0.75rem;
  background: rgba(240, 189, 30, 0.1);
  border-radius: 10px;
  border-left: 3px solid #f0bd1e;
}

.spinner-border {
  width: 1rem;
  height: 1rem;
}

@media (max-width: 1200px) {
  .form-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .form-main-title {
    font-size: 1.5rem;
  }
  
  .top-bar-inner {
    flex-direction: column;
    gap: 1rem;
  }
  
  .top-actions {
    width: 100%;
    flex-direction: column;
  }
  
  .btn-cancel,
  .btn-save {
    width: 100%;
  }
  
  .contner-inner {
    padding: 1.5rem;
  }
}
</style>
