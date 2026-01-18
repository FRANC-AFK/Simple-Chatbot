function appendMessage(sender, text, type = null) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = sender;
  
  let badgeHTML = "";
  if (sender === "bot" && type) {
    const badges = {
      "ai": { emoji: "✨", label: "AI-Enhanced", color: "#17a2b8" },
      "rule": { emoji: "✓", label: "Verified", color: "#28a745" },
      "cached": { emoji: "⚡", label: "Cached", color: "#6610f2" },
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

async function sendTemplateMessage(message, retries = 2) {
  appendMessage("user", message);
  showLoading();

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout

      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (response.status === 429) {
        removeLoading();
        appendMessage("bot", "⏱️ Please wait a moment before sending another message.", "fallback");
        return;
      }

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      removeLoading();
      appendMessage("bot", data.reply, data.type);
      return;

    } catch (error) {
      console.error(`Attempt ${attempt + 1} failed:`, error);
      
      if (attempt === retries) {
        removeLoading();
        appendMessage("bot", "❌ Connection error. Please try again.", "fallback");
      } else {
        // Wait before retry (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, 1000 * (attempt + 1)));
      }
    }
  }
}

function sendUserMessage(event) {
  if (event) event.preventDefault();
  
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  
  if (!message) return;
  
  input.value = "";
  sendTemplateMessage(message);
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
