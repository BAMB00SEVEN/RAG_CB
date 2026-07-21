const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question-input");
const sendBtn = document.getElementById("send-btn");

function addMessage(text, sender, sources = []) {
  const el = document.createElement("div");
  el.className = `message ${sender}`;
  el.textContent = text;

  if (sources.length > 0) {
    const src = document.createElement("div");
    src.className = "sources";
    src.textContent = `Sources: ${sources.join(", ")}`;
    el.appendChild(src);
  }

  chatWindow.appendChild(el);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return el;
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = questionInput.value.trim();
  if (!question) return;

  addMessage(question, "user");
  questionInput.value = "";
  sendBtn.disabled = true;

  const loadingEl = addMessage("Thinking...", "bot");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Something went wrong.");
    }

    const data = await res.json();
    loadingEl.remove();
    addMessage(data.answer, "bot", data.sources || []);
  } catch (err) {
    loadingEl.remove();
    addMessage(`Error: ${err.message}`, "bot");
  } finally {
    sendBtn.disabled = false;
    questionInput.focus();
  }
});
