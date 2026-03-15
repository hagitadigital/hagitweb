(function () {
  "use strict";

const AGENT_URL = "https://brandos.hagitantebi.co.il/api/hagit-agent";
  const STYLES = `
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Jost:wght@300;400&display=swap');

    #hagit-agent-btn {
      position: fixed;
      bottom: 28px;
      right: 28px;
      width: 58px;
      height: 58px;
      border-radius: 50%;
      background: linear-gradient(135deg, #b87333 0%, #8B5E3C 100%);
      border: none;
      cursor: pointer;
      z-index: 9999;
      box-shadow: 0 4px 20px rgba(139,94,60,0.45);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.25s ease, box-shadow 0.25s ease;
      outline: none;
    }
    #hagit-agent-btn:hover {
      transform: scale(1.08);
      box-shadow: 0 6px 28px rgba(139,94,60,0.6);
    }
    #hagit-agent-btn svg {
      width: 26px;
      height: 26px;
      fill: #fdf8f2;
      transition: opacity 0.2s;
    }
    #hagit-agent-btn.open svg.icon-chat { display: none; }
    #hagit-agent-btn:not(.open) svg.icon-close { display: none; }

    #hagit-agent-panel {
      position: fixed;
      bottom: 100px;
      right: 28px;
      width: 340px;
      max-height: 520px;
      background: #fdf8f2;
      border: 1px solid #d4a87a;
      border-radius: 2px;
      box-shadow: 0 12px 48px rgba(100,60,20,0.18);
      z-index: 9998;
      display: flex;
      flex-direction: column;
      font-family: 'Jost', sans-serif;
      overflow: hidden;
      transform: translateY(16px) scale(0.97);
      opacity: 0;
      pointer-events: none;
      transition: transform 0.28s cubic-bezier(.4,0,.2,1), opacity 0.28s ease;
    }
    #hagit-agent-panel.visible {
      transform: translateY(0) scale(1);
      opacity: 1;
      pointer-events: all;
    }

    .ha-header {
      background: linear-gradient(135deg, #8B5E3C 0%, #b87333 100%);
      padding: 14px 18px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .ha-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(253,248,242,0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Cormorant Garamond', serif;
      font-size: 16px;
      color: #fdf8f2;
      font-weight: 300;
      letter-spacing: 0.5px;
      flex-shrink: 0;
      border: 1px solid rgba(253,248,242,0.3);
    }
    .ha-header-text {
      flex: 1;
    }
    .ha-header-name {
      font-family: 'Cormorant Garamond', serif;
      font-size: 15px;
      color: #fdf8f2;
      font-weight: 400;
      letter-spacing: 0.5px;
      line-height: 1.2;
    }
    .ha-header-sub {
      font-size: 10px;
      color: rgba(253,248,242,0.7);
      font-weight: 300;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-top: 2px;
    }
    .ha-status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #7ecba1;
      box-shadow: 0 0 6px #7ecba1;
      flex-shrink: 0;
    }

    .ha-messages {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      direction: rtl;
      scrollbar-width: thin;
      scrollbar-color: #d4a87a transparent;
    }
    .ha-messages::-webkit-scrollbar { width: 4px; }
    .ha-messages::-webkit-scrollbar-thumb { background: #d4a87a; border-radius: 2px; }

    .ha-msg {
      max-width: 88%;
      padding: 10px 13px;
      border-radius: 2px;
      font-size: 13px;
      line-height: 1.6;
      letter-spacing: 0.2px;
      animation: ha-fadein 0.22s ease;
    }
    @keyframes ha-fadein {
      from { opacity: 0; transform: translateY(6px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .ha-msg.bot {
      background: #fff;
      border: 1px solid #e8d5c0;
      color: #4a3020;
      align-self: flex-start;
      border-radius: 2px 12px 12px 12px;
    }
    .ha-msg.user {
      background: linear-gradient(135deg, #8B5E3C, #b87333);
      color: #fdf8f2;
      align-self: flex-end;
      border-radius: 12px 2px 12px 12px;
      font-weight: 300;
    }
    .ha-msg.typing {
      background: #fff;
      border: 1px solid #e8d5c0;
      align-self: flex-start;
      border-radius: 2px 12px 12px 12px;
      padding: 12px 16px;
    }
    .ha-typing-dots {
      display: flex;
      gap: 5px;
      align-items: center;
    }
    .ha-typing-dots span {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #b87333;
      animation: ha-bounce 1.2s infinite ease-in-out;
    }
    .ha-typing-dots span:nth-child(2) { animation-delay: 0.2s; }
    .ha-typing-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes ha-bounce {
      0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
      30% { transform: translateY(-5px); opacity: 1; }
    }

    .ha-quick-replies {
      padding: 0 16px 10px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      direction: rtl;
    }
    .ha-quick-btn {
      background: transparent;
      border: 1px solid #d4a87a;
      color: #8B5E3C;
      font-family: 'Jost', sans-serif;
      font-size: 11px;
      font-weight: 300;
      letter-spacing: 0.5px;
      padding: 5px 10px;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }
    .ha-quick-btn:hover {
      background: #b87333;
      border-color: #b87333;
      color: #fdf8f2;
    }

    .ha-input-row {
      border-top: 1px solid #e8d5c0;
      padding: 12px 14px;
      display: flex;
      gap: 8px;
      align-items: center;
      direction: rtl;
      background: #fdf8f2;
    }
    .ha-input {
      flex: 1;
      border: 1px solid #d4a87a;
      background: #fff;
      border-radius: 2px;
      padding: 9px 12px;
      font-family: 'Jost', sans-serif;
      font-size: 13px;
      font-weight: 300;
      color: #4a3020;
      outline: none;
      direction: rtl;
      transition: border-color 0.2s;
      resize: none;
    }
    .ha-input:focus { border-color: #b87333; }
    .ha-input::placeholder { color: #c4a882; }
    .ha-send-btn {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: linear-gradient(135deg, #b87333, #8B5E3C);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: transform 0.2s, box-shadow 0.2s;
      outline: none;
    }
    .ha-send-btn:hover { transform: scale(1.08); box-shadow: 0 3px 12px rgba(139,94,60,0.4); }
    .ha-send-btn:disabled { opacity: 0.5; cursor: default; transform: none; }
    .ha-send-btn svg { width: 16px; height: 16px; fill: #fdf8f2; }

    .ha-footer {
      text-align: center;
      font-size: 10px;
      color: #c4a882;
      padding: 0 0 10px;
      letter-spacing: 1px;
      font-weight: 300;
    }

    @media (max-width: 480px) {
      #hagit-agent-panel { width: calc(100vw - 32px); right: 16px; bottom: 90px; }
      #hagit-agent-btn { right: 16px; bottom: 16px; }
    }
  `;

  const ICON_CHAT = `<svg class="icon-chat" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/></svg>`;
  const ICON_CLOSE = `<svg class="icon-close" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>`;
  const ICON_SEND = `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>`;

  const WELCOME = "שלום! אני הסוכן של חגית 👋\nאיך אוכל לעזור לך היום? אפשר לשאול על BrandOS, שירותים, תיק עבודות או לתאם פגישה.";

  const QUICK_REPLIES = ["מה זה BrandOS?", "מה השירותים?", "כמה זה עולה?", "תיאום פגישה"];

  let messages = [];
  let isOpen = false;
  let isTyping = false;

  function init() {
    // Inject styles
    const style = document.createElement("style");
    style.textContent = STYLES;
    document.head.appendChild(style);

    // Create button
    const btn = document.createElement("button");
    btn.id = "hagit-agent-btn";
    btn.setAttribute("aria-label", "פתח צ'אט");
    btn.innerHTML = ICON_CHAT + ICON_CLOSE;
    btn.addEventListener("click", togglePanel);
    document.body.appendChild(btn);

    // Create panel
    const panel = document.createElement("div");
    panel.id = "hagit-agent-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "צ'אט עם סוכן חגית");
    panel.innerHTML = `
      <div class="ha-header">
        <div class="ha-avatar">ח</div>
        <div class="ha-header-text">
          <div class="ha-header-name">חגית אנטבי</div>
          <div class="ha-header-sub">Brand Worlds Studio</div>
        </div>
        <div class="ha-status-dot"></div>
      </div>
      <div class="ha-messages" id="ha-messages"></div>
      <div class="ha-quick-replies" id="ha-quick-replies"></div>
      <div class="ha-input-row">
        <button class="ha-send-btn" id="ha-send" aria-label="שלח">${ICON_SEND}</button>
        <input class="ha-input" id="ha-input" type="text" placeholder="כתוב הודעה..." maxlength="300" />
      </div>
      <div class="ha-footer">BRAND WORLDS STUDIO · AI AGENT</div>
    `;
    document.body.appendChild(panel);

    // Wire up events
    const input = document.getElementById("ha-input");
    const sendBtn = document.getElementById("ha-send");
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });
    sendBtn.addEventListener("click", sendMessage);

    // Render quick replies
    renderQuickReplies();

    // Show welcome message
    appendMessage("bot", WELCOME);
  }

  function togglePanel() {
    isOpen = !isOpen;
    const panel = document.getElementById("hagit-agent-panel");
    const btn = document.getElementById("hagit-agent-btn");
    panel.classList.toggle("visible", isOpen);
    btn.classList.toggle("open", isOpen);
    if (isOpen) {
      setTimeout(() => document.getElementById("ha-input").focus(), 300);
    }
  }

  function renderQuickReplies() {
    const container = document.getElementById("ha-quick-replies");
    container.innerHTML = "";
    QUICK_REPLIES.forEach((text) => {
      const btn = document.createElement("button");
      btn.className = "ha-quick-btn";
      btn.textContent = text;
      btn.addEventListener("click", () => {
        container.innerHTML = "";
        sendUserMessage(text);
      });
      container.appendChild(btn);
    });
  }

  function appendMessage(role, text) {
    const container = document.getElementById("ha-messages");
    const div = document.createElement("div");
    div.className = `ha-msg ${role}`;
    div.innerHTML = text
  .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  .replace(/\n/g, '<br>');

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
  }

  function showTyping() {
    const container = document.getElementById("ha-messages");
    const div = document.createElement("div");
    div.className = "ha-msg typing";
    div.id = "ha-typing";
    div.innerHTML = `<div class="ha-typing-dots"><span></span><span></span><span></span></div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
  }

  function removeTyping() {
    const el = document.getElementById("ha-typing");
    if (el) el.remove();
  }

  async function sendUserMessage(text) {
    if (!text.trim() || isTyping) return;

    appendMessage("user", text);
    messages.push({ role: "user", content: text });

    isTyping = true;
    document.getElementById("ha-send").disabled = true;
    showTyping();

    try {
      const response = await fetch(AGENT_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages }),
      });

      const data = await response.json();
      removeTyping();

      const reply = data.reply || "מצטערת, הייתה שגיאה. נסי שוב.";
      appendMessage("bot", reply);
      messages.push({ role: "assistant", content: reply });

    } catch (err) {
      removeTyping();
      appendMessage("bot", "נראה שיש בעיית חיבור. אפשר ליצור קשר ישירות עם חגית 💌");
    }

    isTyping = false;
    document.getElementById("ha-send").disabled = false;
  }

  function sendMessage() {
    const input = document.getElementById("ha-input");
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendUserMessage(text);
  }

  // Init on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
