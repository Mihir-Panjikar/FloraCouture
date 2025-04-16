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
  alert("Logged in! (This is frontend-only, so no real auth.)");
  // Redirect or do something
  return false;
}

function signupUser(event) {
  event.preventDefault();
  alert("Signed up successfully!");
  // You could store fake users in localStorage if needed
  return false;
}
