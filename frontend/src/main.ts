import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

// Helper to get CSRF token from cookies
function getCSRFToken(): string | null {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') return value;
  }
  return null;
}

const app = createApp(App);

app.config.globalProperties.$fetch = (url: string, options: RequestInit = {}) => {
  const csrfToken = getCSRFToken();
  return fetch(url, {
    ...options,
    credentials: 'include', // Ensures cookies are sent
    headers: {
      ...options.headers,
      'X-CSRFToken': csrfToken || '', // Add CSRF token
    },
  });
};

app.use(router);
app.mount('#app');
