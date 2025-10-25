import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import NewQuizPage from '@/views/NewQuizPage.vue';
import QuestionsManager from '@/views/QuestionsManager.vue';
import ScorePage from '@/views/ScorePage.vue';
import AdminLogin from '@/views/AdminLogin.vue';
import AdminQuestions from '@/views/AdminQuestions.vue';
import AdminQuestionForm from '@/views/AdminQuestionForm.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/new-quiz',
      name: 'NewQuizPage',
      component: NewQuizPage,
    },
    {
      path: '/questions',
      name: 'QuestionsManager',
      component: QuestionsManager,
    },
    {
      path: '/score',
      name: 'ScorePage',
      component: ScorePage,
    },
    {
      path: '/admin/login',
      name: 'AdminLogin',
      component: AdminLogin,
    },
    {
      path: '/admin/questions',
      name: 'AdminQuestions',
      component: AdminQuestions,
    },
    {
      path: '/admin/questions/create',
      name: 'AdminQuestionCreate',
      component: AdminQuestionForm,
    },
    {
      path: '/admin/questions/edit/:id',
      name: 'AdminQuestionEdit',
      component: AdminQuestionForm,
    },
  ],
});

export default router;
