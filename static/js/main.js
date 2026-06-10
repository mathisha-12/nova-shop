// Theme toggle
const root = document.documentElement;
const saved = localStorage.getItem("theme") || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
root.dataset.theme = saved;
document.getElementById("theme-toggle").textContent = saved === "dark" ? "☀️" : "🌙";
document.getElementById("theme-toggle").addEventListener("click", () => {
  const next = root.dataset.theme === "dark" ? "light" : "dark";
  root.dataset.theme = next;
  localStorage.setItem("theme", next);
  document.getElementById("theme-toggle").textContent = next === "dark" ? "☀️" : "🌙";
});

// Toast auto-hide
const toast = document.querySelector(".toast");
if (toast) setTimeout(() => toast.remove(), 2500);

// Chatbot
const fab = document.getElementById("chat-fab");
const panel = document.getElementById("chat-panel");
const msgs = document.getElementById("chat-msgs");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
fab.addEventListener("click", () => panel.hidden = !panel.hidden);
document.getElementById("chat-close").addEventListener("click", () => panel.hidden = true);
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim(); if (!text) return;
  add("user", text); input.value = "";
  const r = await fetch("/api/chat", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({ message: text }) });
  const data = await r.json();
  setTimeout(() => add("bot", data.reply), 300);
});
function add(role, text) {
  const d = document.createElement("div");
  d.className = "msg " + role; d.textContent = text;
  msgs.appendChild(d); msgs.scrollTop = msgs.scrollHeight;
}
