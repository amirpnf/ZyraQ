<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-0">
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

    <footer class="mt-auto py-4 bg-dark text-light">
      <div class="container text-center">
        <p class="mb-0 small">
          © 2025 ZyraQ
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

#app > :nth-child(2) {
  flex: 1;
}

.brand-text {
  font-size: 1.5rem;
  letter-spacing: 2px;
  font-weight: 700;
}

.admin-link {
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: all 0.3s;
}

.admin-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>

