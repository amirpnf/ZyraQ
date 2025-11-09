<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg mb-0 custom-navbar">
      <div class="container">
        <router-link to="/" class="navbar-brand fw-bold">
          <span class="brand-text">ZyraQ</span>
        </router-link>
        <div class="navbar-nav ms-auto">
          <router-link to="/admin/login" class="nav-link admin-link">
            Admin
          </router-link>
        </div>
      </div>
    </nav>

    <RouterView />

    <footer class="mt-auto py-4 custom-footer">
      <div class="container text-center">
        <p class="mb-0 small text-white">
          © 2025 ZyraQ - Quiz Platform
        </p>
      </div>
    </footer>
  </div>
</template>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #090043;
  background-image: url('./assets/bkg.svg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

#app > :nth-child(2) {
  flex: 1;
}

.custom-navbar {
  background: linear-gradient(90deg, #f0bd1e, #cc13b5) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.brand-text {
  font-size: 1.5rem;
  letter-spacing: 2px;
  font-weight: 700;
  color: white !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.navbar-brand {
  color: white !important;
}

.admin-link {
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  transition: all 0.3s;
  color: white !important;
  font-weight: 500;
}

.admin-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: white !important;
}

.custom-footer {
  background: linear-gradient(90deg, #cc13b5, #f0bd1e);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
}

.custom-footer p {
  margin: 0;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>

