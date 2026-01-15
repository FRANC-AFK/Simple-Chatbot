function appendMessage(sender, text, type = null) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = sender;
  
  let badgeHTML = "";
  if (sender === "bot" && type) {
    const badges = {
      "ai": { emoji: "✨", label: "AI-Enhanced", color: "#17a2b8" },
      "rule": { emoji: "✓", label: "Verified", color: "#28a745" },
      "fallback": { emoji: "⚠️", label: "Limited", color: "#ffc107" }
    };
    
    const badge = badges[type] || badges["rule"];
    badgeHTML = `<span class="response-badge" style="background: ${badge.color};">${badge.emoji} ${badge.label}</span>`;
  }
  
  msg.innerHTML = `${badgeHTML}${text}`;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showLoading() {
  const chatBox = document.getElementById("chat-box");
  const loader = document.createElement("div");
  loader.className = "bot loading";
  loader.innerHTML = '<span class="dots"><span></span><span></span><span></span></span>';
  loader.id = "loading-indicator";
  chatBox.appendChild(loader);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeLoading() {
  const loader = document.getElementById("loading-indicator");
  if (loader) loader.remove();
}

function sendTemplateMessage(message) {
  appendMessage("user", message);
  showLoading();

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
    .then(res => res.json())
    .then(data => {
      removeLoading();
      appendMessage("bot", data.reply, data.type);
    })
    .catch(() => {
      removeLoading();
      appendMessage("bot", "Error connecting to server.", "fallback");
    });
}

function sendUserMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  
  if (!message) return;
  
  input.value = "";
  sendTemplateMessage(message);
}

function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendUserMessage();
  }
}

// Debug: Check HuggingFace status on page load
async function checkHFStatus() {
  try {
    const response = await fetch("/debug/hf");
    const data = await response.json();
    
    // Show in console
    console.log("HuggingFace Status:", data);
    
    // Show in UI if HF is working
    if (data.hf_working) {
      appendMessage("bot", "✨ HuggingFace API is connected and working!", "ai");
    } else {
      appendMessage("bot", "⚠️ HuggingFace API offline - using rule-based responses only", "fallback");
    }
  } catch (error) {
    console.error("Failed to check HF status:", error);
  }
}

// Check HF status on page load
window.addEventListener("load", checkHFStatus);
