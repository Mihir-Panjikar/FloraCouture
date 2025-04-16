// index.js — JavaScript for Bloomify Home Page

// Load chatbot into placeholder on page load
document.addEventListener("DOMContentLoaded", () => {
  fetch("/chatbot/")
    .then(res => res.text())
    .then(html => {
      document.getElementById("chatbot-placeholder").innerHTML = html;
    })
    .catch(err => {
      console.error("Failed to load chatbot:", err);
    });
});
