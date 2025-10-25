import axios from 'axios';

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true,
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      'Content-Type': 'application/json',
    };
    if (token != null) {
      headers.authorization = 'Bearer ' + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
        throw error;
      });
  },
  getQuizInfo() {
    return this.call('get', 'quiz-info');
  },
  getQuestion(position, token = null) {
    return this.call('get', `questions?position=${position}`, null, token);
  },
  postParticipation(playerName, answers) {
    return this.call('post', 'participations', {
      playerName: playerName,
      answers: answers,
    });
  },
  // Admin
  login(password) {
    return this.call('post', 'login', { password });
  },
  getQuestionById(questionId, token) {
    return this.call('get', `questions/${questionId}`, null, token);
  },
  createQuestion(questionData, token) {
    return this.call('post', 'questions', questionData, token);
  },
  updateQuestion(questionId, questionData, token) {
    return this.call('put', `questions/${questionId}`, questionData, token);
  },
  deleteQuestion(questionId, token) {
    return this.call('delete', `questions/${questionId}`, null, token);
  },
  deleteAllQuestions(token) {
    return this.call('delete', 'questions/all', null, token);
  },
  deleteAllParticipations(token) {
    return this.call('delete', 'participations/all', null, token);
  },
  rebuildDatabase(token) {
    return this.call('post', 'rebuild-db', null, token);
  },
};
