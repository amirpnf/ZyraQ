export default {
  saveToken(token) {
    window.localStorage.setItem('adminToken', token);
  },
  getToken() {
    return window.localStorage.getItem('adminToken');
  },
  clearToken() {
    window.localStorage.removeItem('adminToken');
  },
  isAuthenticated() {
    return this.getToken() !== null;
  },
};
