const loginToggle = document.getElementById("loginToggle");
const signupToggle = document.getElementById("signupToggle");
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");

loginToggle.addEventListener("click", () => {
  loginToggle.classList.add("active");
  signupToggle.classList.remove("active");
  loginForm.classList.remove("hidden");
  signupForm.classList.add("hidden");
});

signupToggle.addEventListener("click", () => {
  signupToggle.classList.add("active");
  loginToggle.classList.remove("active");
  signupForm.classList.remove("hidden");
  loginForm.classList.add("hidden");
});

function loginUser(event) {
  event.preventDefault();
  
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  
  // Call the Django API endpoint
  fetch('/api/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      email: email,
      password: password
    })
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Login failed');
  })
  .then(data => {
    // Store token in localStorage
    localStorage.setItem('authToken', data.token);
    window.location.href = '/';
  })
  .catch(error => {
    alert('Login failed. Please check your credentials.');
    console.error('Error:', error);
  });
  
  return false;
}

function signupUser(event) {
  event.preventDefault();
  
  const email = document.getElementById('signup-email').value;
  const password = document.getElementById('signup-password').value;
  
  // Call the Django API endpoint
  fetch('/api/register/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      email: email,
      password: password
    })
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Registration failed');
  })
  .then(data => {
    alert('Registration successful! Please log in.');
    // Switch to login form
    loginToggle.click();
  })
  .catch(error => {
    alert('Registration failed. Please try again.');
    console.error('Error:', error);
  });
  
  return false;
}

// Function to get CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
