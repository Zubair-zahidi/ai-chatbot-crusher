const chatContainer = document.getElementById("chatContainer");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");

// Append messages to chat
function appendMessage(sender, text) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);
  messageDiv.innerHTML = `<div class="bubble">${text}</div>`;
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Append images to chat
function appendImage(url, name) {
  const imgDiv = document.createElement("div");
  imgDiv.classList.add("message", "bot");
  imgDiv.innerHTML = `<div class="bubble"><strong>${name}</strong><br><img src="${url}" alt="${name}" style="max-width:300px; border-radius:8px;" /></div>`;
  chatContainer.appendChild(imgDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Typing indicator
function showTyping() {
  const typingDiv = document.createElement("div");
  typingDiv.classList.add("message", "bot", "typing");
  typingDiv.innerHTML = `<div class="bubble">...</div>`;
  chatContainer.appendChild(typingDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  return typingDiv;
}

// Send message
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  userInput.value = "";

  const typingDiv = showTyping();

  try {
    // Detect image queries
    if (message.toLowerCase().includes("show me") || message.toLowerCase().includes("image of")) {
      // Clean query for Unsplash
      let query = message.toLowerCase()
                         .replace("show me image of", "")
                         .replace("show me", "")
                         .replace("image of", "")
                         .trim();

      const res = await fetch("/image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      });
      const data = await res.json();
      typingDiv.remove();

      if (data.image_url) {
        appendImage(data.image_url, data.image_name);
      } else {
        appendMessage("bot", "Sorry, I couldn't find an image for that.");
      }
      return;
    }

    // Regular text query
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await res.json();

    let botText = "";
    typingDiv.querySelector(".bubble").textContent = "";
    for (let char of data.response) {
      botText += char;
      typingDiv.querySelector(".bubble").textContent = botText;
      await new Promise(r => setTimeout(r, 15));
    }
    typingDiv.classList.remove("typing");

  } catch (error) {
    typingDiv.querySelector(".bubble").textContent = "Oops! Something went wrong.";
    typingDiv.classList.remove("typing");
  }
}

// Event listeners
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

// Theme toggle
const themeToggle = document.getElementById("themeToggle");
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
  document.body.classList.toggle("dark-mode");
  themeToggle.textContent = document.body.classList.contains("light-mode") ? "🌞" : "🌙";
});

// Voice input
let recognition;
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => micBtn.classList.add("listening");
  recognition.onend = () => micBtn.classList.remove("listening");

  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    userInput.value = transcript;
    sendMessage();
  };

  recognition.onerror = function(event) {
    console.error("Speech recognition error:", event.error);
  };

  micBtn.addEventListener("click", () => recognition.start());

} else {
  micBtn.disabled = true;
  alert("Your browser does not support speech recognition.");
}

const canvas = document.getElementById("bg");
const ctx = canvas.getContext("2d");
canvas.width = innerWidth;
canvas.height = innerHeight;
let particles = Array.from({ length: 40 }, () => ({
  x: Math.random() * canvas.width,
  y: Math.random() * canvas.height,
  r: Math.random() * 2 + 0.5,
  dx: (Math.random() - 0.5) * 0.6,
  dy: (Math.random() - 0.5) * 0.6
}));
function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "rgba(0,255,255,0.6)";
  particles.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fill();
    p.x += p.dx;
    p.y += p.dy;
    if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
    if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
  });
  requestAnimationFrame(animate);
}
animate();

window.addEventListener("load", () => {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "light") document.body.classList.add("light-mode");
  else document.body.classList.add("dark-mode");
});

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
  document.body.classList.toggle("dark-mode");
  const mode = document.body.classList.contains("light-mode") ? "light" : "dark";
  localStorage.setItem("theme", mode);
  themeToggle.textContent = mode === "light" ? "🌞" : "🌙";
});


messageDiv.innerHTML = `<div class="bubble" data-time="${new Date().toLocaleTimeString()}">${text}</div>`;
