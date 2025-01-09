export function getCSRFToken() {
    const csrfCookie = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
    if (csrfCookie) {
        console.log('CSRF token from cookie:', csrfCookie.split('=')[1]);
        return csrfCookie.split('=')[1];  
    }
    console.log('CSRF token not found in cookies');
    return null;  
  }
  