import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Toast, { POSITION } from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
// Toast options
const toastOptions = {
    position: POSITION.TOP_RIGHT, // Use POSITION.TOP_RIGHT instead of a string
    timeout: 3000,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
};
const app = createApp(App);
// Helper to get CSRF token from cookies
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken')
            return value;
    }
    return null;
}
app.config.globalProperties.$fetch = (url, options = {}) => {
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
app.use(Toast, toastOptions); // Use toast plugin
app.mount('#app');
