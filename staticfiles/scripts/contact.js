// contact.js — JavaScript for Contact Page

document.addEventListener("DOMContentLoaded", () => {
    // Load chatbot
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
  
    // Handle form submission
    const form = document.querySelector(".contact-form");
    if (form) {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
  
        const name = form.querySelector('input[placeholder="Your Name"]').value.trim();
        const contact = form.querySelector('input[placeholder="Your Contact (Phone or Email)"]').value.trim();
        const message = form.querySelector("textarea").value.trim();
  
        if (!name || !contact || !message) {
          alert("Please fill in all fields!");
          return;
        }
  
        // Simulate sending message
        alert("Thank you for reaching out, " + name + "! We'll get back to you soon.");
        form.reset();
      });
    }
  });
  