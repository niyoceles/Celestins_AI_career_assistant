"""Styling constants for the Celestin NIYONSABA Career Gradio app."""

GOLD = "#ecad0a"
BLUE = "#209dd7"
PURPLE = "#753991"

EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

CSS = """
:root {
  --twin-gold: #ecad0a;
  --twin-blue: #209dd7;
  --twin-purple: #753991;
  --twin-bg: #0d0d10;
  --twin-surface: #16161b;
  --twin-surface-2: #1c1c22;
  --twin-border: #2a2a32;
  --twin-border-strong: #3a3a44;
  --twin-text: #ececef;
  --twin-muted: #8c8c95;
}

/* Light mode: Gradio adds `.dark` to <body> when dark; absence = light.
   Only the neutral palette flips — gold/blue/purple accents stay identical. */
body:not(.dark) {
  --twin-bg: #f4f4f6;
  --twin-surface: #ffffff;
  --twin-surface-2: #ededf0;
  --twin-border: #dcdce2;
  --twin-border-strong: #b8b8c0;
  --twin-text: #1a1a20;
  --twin-muted: #6a6a72;
}

footer, .built-with, .show-api, .api-docs { display: none !important; }

html, body, gradio-app { background: var(--twin-bg) !important; }

/* ---------- Stable layout ---------- */
.gradio-container {
  background: var(--twin-bg) !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  width: 100% !important;
  max-width: 880px !important;
  min-width: 0 !important;
  margin: 0 auto !important;
  padding: 32px 24px 48px !important;
}
.gradio-container .main, .gradio-container .contain, .gradio-container .wrap {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
}
.gradio-container * { min-width: 0; }

/* ---------- Title ---------- */
.gradio-container h1 {
  color: var(--twin-text) !important;
  font-size: 26px !important;
  font-weight: 700 !important;
  letter-spacing: -0.02em !important;
  border-left: 3px solid var(--twin-gold);
  padding-left: 12px !important;
  margin: 4px 0 8px !important;
  text-align: left !important;
}

/* ---------- Sharp corners on structural pieces ---------- */
.chatbot, .chatbot *, .block, .form,
button, input, textarea,
.examples button {
  border-radius: 0 !important;
}

/* ---------- Block surfaces ---------- */
.block, .form { background: transparent !important; box-shadow: none !important; }

/* ---------- Hide the Chatbot label / header strip ---------- */
.chatbot > .block-label,
.chatbot > label,
.chatbot .label-wrap,
.chatbot .block-label,
.chatbot > .label-container {
  display: none !important;
}

/* ---------- Chatbot frame ---------- */
.chatbot, .chatbot.block {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  min-height: 460px !important;
  box-shadow: none !important;
}
.chatbot .placeholder, .chatbot .placeholder * { color: var(--twin-muted) !important; }

/* ---------- Message rows: strip parent backgrounds ---------- */
.message-row,
.message-row > div,
.message-row .role,
.message-wrap, .bubble-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* ---------- Reset borders on every bubble variant first ---------- */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  border: 0 !important;
  box-shadow: none !important;
  padding: 6px 10px !important;
}

/* ---------- Bubble backgrounds (broad to cover Gradio variants) ---------- */
.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: var(--twin-blue) !important;
  color: #ffffff !important;
}

.message-row.bot-row .message,
.message-row.bot-row .message-bubble,
.message-row.bot-row .bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--twin-surface-2) !important;
  color: var(--twin-text) !important;
}

/* ---------- Purple stripe ----------
   Apply to every common bubble class for assistant rows (we don't know which
   one the running Gradio uses), then suppress on any *nested* instance so the
   stripe lands on the outermost matching element only — exactly one stripe. */
.message-row.bot-row .message,
.message-row.bot-row .bubble,
.message-row.bot-row .message-bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .bubble,
.message-row[data-role="assistant"] .message-bubble {
  border-left: 2px solid var(--twin-purple) !important;
}

.message-row.bot-row .message .message,
.message-row.bot-row .message .bubble,
.message-row.bot-row .message .message-bubble,
.message-row.bot-row .bubble .message,
.message-row.bot-row .bubble .bubble,
.message-row.bot-row .bubble .message-bubble,
.message-row.bot-row .message-bubble .message,
.message-row.bot-row .message-bubble .bubble,
.message-row.bot-row .message-bubble .message-bubble,
.message-row[data-role="assistant"] .message .message,
.message-row[data-role="assistant"] .message .bubble,
.message-row[data-role="assistant"] .message .message-bubble,
.message-row[data-role="assistant"] .bubble .message,
.message-row[data-role="assistant"] .bubble .bubble,
.message-row[data-role="assistant"] .bubble .message-bubble,
.message-row[data-role="assistant"] .message-bubble .message,
.message-row[data-role="assistant"] .message-bubble .bubble,
.message-row[data-role="assistant"] .message-bubble .message-bubble {
  border-left: 0 !important;
}

/* ---------- Uniform font size in bubbles ----------
   The "first paragraph different size" was caused by a leaky `.prose p:first-of-type`
   selector. Force every paragraph in a bubble to the same size. */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  font-size: 14px !important;
  line-height: 1.55 !important;
}
.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p {
  font-size: 14px !important;
  line-height: 1.55 !important;
  margin: 0 0 8px !important;
  color: inherit !important;
}
.message-row .message p:last-child,
.message-row .message-bubble p:last-child,
.message-row .bubble p:last-child,
.message-row .prose p:last-child { margin-bottom: 0 !important; }

/* Strip stray internal borders/backgrounds from anything inside a bubble */
.message-row .message *,
.message-row .message-bubble *,
.message-row .bubble * {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  color: inherit !important;
}
.message-row .message a,
.message-row .message-bubble a {
  color: var(--twin-gold) !important;
  text-decoration: underline;
}

/* ---------- Input row alignment ---------- */
.input-row,
.gr-input-row,
.chat-input-row,
form[class*="input"] { align-items: stretch !important; }

textarea, input[type="text"] {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 14px !important;
  padding: 12px 14px !important;
  line-height: 1.4 !important;
  min-height: 48px !important;
}
textarea:focus, input[type="text"]:focus {
  border-color: var(--twin-gold) !important;
  outline: none !important;
  box-shadow: 0 0 0 1px var(--twin-gold) !important;
}
textarea::placeholder, input::placeholder { color: var(--twin-muted) !important; }

/* ---------- Buttons ---------- */
button {
  font-family: 'JetBrains Mono', 'SF Mono', Menlo, monospace !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  border: 1px solid var(--twin-border) !important;
  background: transparent !important;
  color: var(--twin-text) !important;
  padding: 0 16px !important;
  min-height: 48px !important;
  align-self: stretch !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer;
  transition: background 0.12s ease, color 0.12s ease, border-color 0.12s ease;
}
button:hover { border-color: var(--twin-gold) !important; color: var(--twin-gold) !important; }

button.primary,
button[variant="primary"],
button.submit,
button.submit-button,
.submit-button,
button.lg.primary {
  background: var(--twin-gold) !important;
  border: 1px solid var(--twin-gold) !important;
  color: #111111 !important;
  min-height: 48px !important;
  align-self: stretch !important;
  padding: 0 14px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
button.primary:hover,
button.submit:hover,
.submit-button:hover,
button.lg.primary:hover {
  background: #ffc320 !important;
  border-color: #ffc320 !important;
  color: #111111 !important;
}

/* ---------- Submit-button icon: center vertically and size correctly ---------- */
button.submit svg,
button.submit-button svg,
.submit-button svg,
button.primary svg,
button[variant="primary"] svg {
  width: 18px !important;
  height: 18px !important;
  margin: 0 auto !important;
  display: block !important;
  align-self: center !important;
  color: #111111 !important;
  fill: currentColor !important;
  stroke: currentColor !important;
}

/* ---------- Examples ---------- */
.examples, .examples-holder, [data-testid="examples"] {
  background: transparent !important;
  padding: 0 !important;
  margin-top: 14px !important;
}
.examples table, .examples-table { background: transparent !important; border: 0 !important; }
.examples button, .example, .examples td button, [data-testid="examples"] button {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  color: var(--twin-text) !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  padding: 10px 14px !important;
  text-align: left !important;
  min-height: 0 !important;
  align-self: auto !important;
  display: inline-block !important;
}
.examples button:hover, .example:hover, [data-testid="examples"] button:hover {
  border-color: var(--twin-blue) !important;
  color: var(--twin-blue) !important;
  background: var(--twin-surface) !important;
}

/* ---------- Icon buttons (clear, retry, copy) ---------- */
.icon-button, .chatbot .icon-button {
  color: var(--twin-muted) !important;
  background: transparent !important;
  border: 0 !important;
  min-height: 0 !important;
  align-self: auto !important;
  padding: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.icon-button:hover, .chatbot .icon-button:hover { color: var(--twin-gold) !important; }

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--twin-bg); }
::-webkit-scrollbar-thumb { background: var(--twin-border-strong); }
::-webkit-scrollbar-thumb:hover { background: var(--twin-purple); }

/* ---------- Selection ---------- */
::selection { background: var(--twin-gold); color: #111111; }

/* ---------- Mobile ---------- */
@media (max-width: 640px) {
  .gradio-container { padding: 22px 14px 36px !important; }
  .gradio-container h1 { font-size: 22px !important; }
}

/* ---------- Polished, comfortable chat experience ---------- */
:root {
  --twin-bg: #0b1018;
  --twin-surface: #111a25;
  --twin-surface-2: #172332;
  --twin-border: #263647;
  --twin-border-strong: #354b60;
  --twin-text: #f3f6fa;
  --twin-muted: #a2b0c0;
}
body:not(.dark) {
  --twin-bg: #f3f6fa;
  --twin-surface: #ffffff;
  --twin-surface-2: #edf2f7;
  --twin-border: #dce4ed;
  --twin-border-strong: #c4d0dd;
  --twin-text: #182433;
  --twin-muted: #586a7d;
}
html, body, gradio-app {
  background:
    radial-gradient(ellipse at 50% -18%, rgba(32, 157, 215, .13), transparent 46%),
    var(--twin-bg) !important;
}
.gradio-container {
  max-width: 980px !important;
  padding: clamp(24px, 5vw, 52px) clamp(16px, 4vw, 34px) 48px !important;
}
.gradio-container h1 {
  font-size: clamp(28px, 4vw, 38px) !important;
  letter-spacing: -.04em !important;
  border-left: 4px solid var(--twin-gold);
  padding: 2px 0 2px 16px !important;
  margin: 4px 0 12px !important;
}
.gradio-container p { color: var(--twin-muted); }

/* Restore rounded surfaces after the legacy sharp-corner reset above. */
.chatbot, .chatbot.block {
  border-radius: 20px !important;
  border-color: var(--twin-border) !important;
  min-height: min(58vh, 620px) !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, .16) !important;
  overflow: hidden !important;
}
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  border-radius: 16px !important;
  padding: 12px 16px !important;
  line-height: 1.7 !important;
}
.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: linear-gradient(135deg, #188bc4, #2574b8) !important;
  border: 1px solid rgba(255, 255, 255, .12) !important;
  border-radius: 16px 16px 4px 16px !important;
}
.message-row.bot-row .message,
.message-row.bot-row .bubble,
.message-row.bot-row .message-bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .bubble,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--twin-surface-2) !important;
  border: 1px solid var(--twin-border) !important;
  border-left: 3px solid var(--twin-purple) !important;
  border-radius: 4px 16px 16px 16px !important;
}
.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p { line-height: 1.7 !important; }

/* Keep controls calm and legible, with a clear primary send action. */
textarea, input[type="text"], .gradio-container select {
  border-radius: 12px !important;
  border-color: var(--twin-border-strong) !important;
  font-size: 15px !important;
  padding: 14px 16px !important;
  transition: border-color .18s ease, box-shadow .18s ease, background .18s ease;
}
textarea:focus, input[type="text"]:focus, .gradio-container select:focus {
  border-color: var(--twin-blue) !important;
  box-shadow: 0 0 0 3px rgba(32, 157, 215, .18) !important;
}
button {
  border-radius: 10px !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  transition: transform .16s ease, background .16s ease, border-color .16s ease, box-shadow .16s ease !important;
}
button:hover { transform: translateY(-1px); }
button.primary, button[variant="primary"], button.submit,
button.submit-button, .submit-button, button.lg.primary {
  border-radius: 10px !important;
  box-shadow: 0 5px 16px rgba(236, 173, 10, .18) !important;
}
.examples button, .example, .examples td button, [data-testid="examples"] button {
  border-radius: 12px !important;
  padding: 12px 15px !important;
  line-height: 1.45 !important;
}
.examples button:hover, .example:hover, [data-testid="examples"] button:hover {
  background: var(--twin-surface-2) !important;
  box-shadow: 0 6px 18px rgba(0, 0, 0, .1) !important;
}
.icon-button, .chatbot .icon-button { border-radius: 8px !important; }
button:focus-visible, a:focus-visible, select:focus-visible, textarea:focus-visible {
  outline: 3px solid rgba(32, 157, 215, .72) !important;
  outline-offset: 2px !important;
}

@media (max-width: 640px) {
  .gradio-container { padding: 24px 14px 30px !important; }
  .chatbot, .chatbot.block { min-height: 54vh !important; border-radius: 16px !important; }
  .message-row .message, .message-row .message-bubble, .message-row .bubble {
    padding: 10px 13px !important;
    max-width: 92% !important;
  }
  .examples button, .example, .examples td button, [data-testid="examples"] button {
    width: 100% !important;
  }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; }
}

/* ---------- ChatGPT-inspired conversation layout ---------- */
html, body, gradio-app { min-height: 100%; }
body { overflow-x: hidden; }
.gradio-container {
  width: 100% !important;
  max-width: 100% !important;
  min-height: 100vh !important;
  padding: 30px 24px 24px !important;
}
.gradio-container .main {
  width: 100% !important;
  max-width: 900px !important;
  min-height: calc(100vh - 54px) !important;
  margin: 0 auto !important;
}
.gradio-container h1 {
  width: fit-content;
  margin: 0 auto 8px !important;
  border-left: 0 !important;
  padding: 0 !important;
  font-size: clamp(22px, 3vw, 28px) !important;
  font-weight: 650 !important;
  letter-spacing: -.035em !important;
  text-align: center !important;
}
.gradio-container .main > p {
  max-width: 620px;
  margin: 0 auto 28px !important;
  color: var(--twin-muted) !important;
  font-size: 15px !important;
  line-height: 1.6 !important;
  text-align: center !important;
}
.chatbot, .chatbot.block {
  width: 100% !important;
  min-height: min(58vh, 620px) !important;
  background: transparent !important;
  border: 0 !important;
  border-radius: 0 !important;
  box-shadow: none !important;
}
.message-row { max-width: 780px !important; margin-left: auto !important; margin-right: auto !important; }
.message-row .message, .message-row .message-bubble, .message-row .bubble {
  font-size: 15px !important;
}
.examples, .examples-holder, [data-testid="examples"] {
  max-width: 780px !important;
  margin: 10px auto 0 !important;
}
.examples button, .example, .examples td button, [data-testid="examples"] button {
  min-height: 52px !important;
  background: var(--twin-surface) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .05) !important;
}
form:has(textarea) {
  position: sticky !important;
  z-index: 5 !important;
  bottom: 0 !important;
  width: 100% !important;
  max-width: 820px !important;
  margin: 18px auto 0 !important;
  padding: 10px !important;
  background: color-mix(in srgb, var(--twin-bg) 88%, transparent) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 20px !important;
  box-shadow: 0 12px 36px rgba(0, 0, 0, .14) !important;
  backdrop-filter: blur(16px);
}
form:has(textarea) textarea {
  min-height: 48px !important;
  max-height: 160px !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  padding: 12px 14px !important;
}
form:has(textarea) textarea:focus { box-shadow: none !important; }
form:has(textarea) button.primary,
form:has(textarea) button[variant="primary"],
form:has(textarea) button.submit,
form:has(textarea) button.submit-button,
form:has(textarea) .submit-button {
  min-width: 46px !important;
  min-height: 46px !important;
  border-radius: 14px !important;
}
form:has(textarea) select {
  min-height: 38px !important;
  padding: 8px 12px !important;
}

@media (max-width: 640px) {
  .gradio-container { padding: 20px 14px 14px !important; }
  .gradio-container .main { min-height: calc(100vh - 34px) !important; }
  .gradio-container .main > p { margin-bottom: 18px !important; font-size: 14px !important; }
  .chatbot, .chatbot.block { min-height: 52vh !important; }
  form:has(textarea) { margin-top: 12px !important; padding: 7px !important; border-radius: 16px !important; }
}
"""

JS = """
() => {
  document.title = 'Celestin NIYONSABA Career';

  const focusInput = () => {
    const areas = document.querySelectorAll('textarea');
    if (areas.length) areas[areas.length - 1].focus();
  };
  setTimeout(focusInput, 300);

  // Re-focus the message field whenever Gradio re-enables it
  // (i.e. after the assistant finishes responding).
  const watchTextarea = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };

  const scan = () => document.querySelectorAll('textarea').forEach(watchTextarea);
  setTimeout(scan, 500);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""
