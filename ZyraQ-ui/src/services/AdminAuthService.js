const TOKEN_KEY = 'adminToken';

export default {
  saveToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  },

  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  clearToken() {
    localStorage.removeItem(TOKEN_KEY);
  },

  isAdminLoggedIn() {
    return !!this.getToken();
  },

  logout() {
    this.clearToken();
  },
};
