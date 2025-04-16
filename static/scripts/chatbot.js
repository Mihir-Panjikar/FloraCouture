// scripts/chatbot.js

document.addEventListener("DOMContentLoaded", () => {
  const chatLog = document.getElementById("chat-log");
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");

  function sendMessage() {
    const message = chatInput.value.trim();
    if (message === "") return;

    // Display user message
    const userMsg = document.createElement("div");
    userMsg.classList.add("user-message");
    userMsg.innerText = message;
    chatLog.appendChild(userMsg);

    // Bot reply (dummy logic)
    const botMsg = document.createElement("div");
    botMsg.classList.add("bot-message");
    botMsg.innerText = getBotReply(message);
    chatLog.appendChild(botMsg);

    chatInput.value = "";
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  function getBotReply(msg) {
    msg = msg.toLowerCase();
    if (msg.includes("hi") || msg.includes("hello")) return "Hello! How can I help you today?";
    if (msg.includes("price") || msg.includes("cost")) return "Our bouquets start at just ₹299!";
    if (msg.includes("custom") || msg.includes("chocolate")) return "You can customize with chocolates, toys, and more!";
    if (msg.includes("thanks")) return "You're welcome! 😊";
    return "Sorry, I didn’t understand. Can you try asking differently?";
  }

  sendBtn.addEventListener("click", sendMessage);
  chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});
