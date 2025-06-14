document.addEventListener("DOMContentLoaded", function () {
  const botButton = document.createElement("div");
  botButton.innerHTML = "🤖";
  botButton.id = "navi-button";
  document.body.appendChild(botButton);

  const chatBox = document.createElement("div");
  chatBox.innerHTML = `
    <div id="navi-header">Cześć, tu Navi!</div>
    <div id="navi-body">
      <div id="navi-log" style="overflow-y: auto; max-height: 260px;"></div>
      <input type="text" id="navi-input" placeholder="Zadaj pytanie..." />
    </div>
  `;
  chatBox.id = "navi-box";
  document.body.appendChild(chatBox);

  botButton.onclick = () => {
    chatBox.classList.toggle("navi-open");
  };

  document.getElementById("navi-input").addEventListener("keypress", async (e) => {
    if (e.key === "Enter") {
      const input = e.target.value;
      if (!input) return;

      const log = document.getElementById("navi-log");
      log.innerHTML += `<div class="user-msg">${input}</div>`;
      e.target.value = "";

      const response = await getResponse(input);
      log.innerHTML += `<div class="bot-msg">${response}</div>`;

      // ⬇️ Automatyczne przewinięcie po dodaniu wiadomości
      setTimeout(() => {
        log.scrollTop = log.scrollHeight;
      }, 100);
    }
  });
});

async function getResponse(userMsg) {
  try {
    const res = await fetch("https://navi-chatbot-1.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMsg })
    });
    const data = await res.json();
    return data.reply;
  } catch (err) {
    return "Ups! Coś poszło nie tak...";
  }
}
