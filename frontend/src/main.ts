import '../../api/axios-config'
import { getCSRFToken } from '../../api/axios-config'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import App from './App.vue'
import router from './router'


import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const csrfToken = getCSRFToken();
if (csrfToken) {
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
  axios.defaults.withCredentials = true;  
  console.log('CSRF Token:', csrfToken);
} else {
  console.error('CSRF token not found!');
}

axios.defaults.withCredentials = true;

axios.defaults.baseURL = 'http://localhost:8000'

const app = createApp(App)

app.use(createPinia())

app.use(router)

app.mount('#app')
