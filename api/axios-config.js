import axios from 'axios';

export const getCSRFToken = () => {
  const match = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
  if (match) {
    return match.split('=')[1]; 
  }
  return null;
};

axios.defaults.withCredentials = true;

axios.interceptors.request.use((config) => {
  const csrfToken = getCSRFToken();
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  } else {
    console.error('CSRF token not found!');
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default axios;
