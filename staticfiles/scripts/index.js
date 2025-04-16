// index.js — JavaScript for Bloomify Home Page

// Load chatbot into placeholder on page load
document.addEventListener("DOMContentLoaded", () => {
    fetch("chatbot.html")
      .then((res) => res.text())
      .then((html) => {
        const chatbotContainer = document.getElementById("chatbot-placeholder");
        if (chatbotContainer) {
          chatbotContainer.innerHTML = html;
        }
      })
      .catch((err) => {
        console.error("Failed to load chatbot:", err);
      });
  });
  