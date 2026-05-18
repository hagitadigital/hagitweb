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

    .ha-link {
      color: #b87333;
      font-weight: 400;
      text-decoration: underline;
      text-underline-offset: 2px;
    }
    .ha-link:hover { color: #8B5E3C; }

    .ha-cta-wa {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(135deg, #25D366, #128C7E);
      color: #fff !important;
      padding: 9px 14px;
      border-radius: 22px;
      font-family: 'Jost', sans-serif;
      font-size: 12px;
      font-weight: 400;
      letter-spacing: 0.5px;
      text-decoration: none;
      margin: 8px 0 2px;
      transition: transform 0.2s, box-shadow 0.2s;
      box-shadow: 0 2px 8px rgba(37,211,102,0.25);
    }
    .ha-cta-wa:hover {
      transform: translateY(-1px);
      box-shadow: 0 5px 16px rgba(37,211,102,0.4);
    }
    .ha-cta-wa svg { flex-shrink: 0; }

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

  const WA_ICON = `<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>`;

  function escapeHtml(s) {
    return s
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderLink(url, label) {
    const safeUrl = url.replace(/"/g, "");
    if (/wa\.me|whatsapp\.com|api\.whatsapp/.test(url)) {
      const text = label && label !== url ? label : "פתח שיחת וואטסאפ";
      return `<a class="ha-cta-wa" href="${safeUrl}" target="_blank" rel="noopener">${WA_ICON}<span>${text}</span></a>`;
    }
    return `<a class="ha-link" href="${safeUrl}" target="_blank" rel="noopener">${label || url}</a>`;
  }

  function formatMessage(text) {
    let html = escapeHtml(text);

    // Markdown links — also tolerant to separators between ] and ( (e.g. "[label] 👉 (url)")
    html = html.replace(
      /\[([^\]]+)\]\s*[^\(]{0,4}\((https?:\/\/[^\s)]+)\)/g,
      (_m, label, url) => renderLink(url, label.trim())
    );

    // Bare URLs not yet linkified
    html = html.replace(/(https?:\/\/[^\s<"]+)/g, (m) => {
      let trail = "";
      let url = m;
      while (/[.,;:!?)\]]$/.test(url)) {
        trail = url.slice(-1) + trail;
        url = url.slice(0, -1);
      }
      return renderLink(url, url) + trail;
    });

    html = html
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br>");

    return html;
  }

  function appendMessage(role, text) {
    const container = document.getElementById("ha-messages");
    const div = document.createElement("div");
    div.className = `ha-msg ${role}`;
    div.innerHTML = role === "user" ? escapeHtml(text).replace(/\n/g, "<br>") : formatMessage(text);
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
