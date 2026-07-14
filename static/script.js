/* ==========================================================================
   FinPilot AI — client logic
   Handles form submission, loading state, lightweight Markdown rendering,
   the Financial Health Score gauge, and copy/download actions.
   ========================================================================== */

const form = document.getElementById("profile-form");
const submitBtn = document.getElementById("submit-btn");

const emptyState = document.getElementById("empty-state");
const loadingState = document.getElementById("loading-state");
const errorState = document.getElementById("error-state");
const errorText = document.getElementById("error-text");
const reportContent = document.getElementById("report-content");

const loadingText = document.getElementById("loading-text");

let lastReportMarkdown = ""; // kept for copy / download actions

// Rotating loading messages to reflect the multi-agent pipeline in progress.
const LOADING_MESSAGES = [
  "Budget Planner Agent is reviewing your income & expenses…",
  "Investment Advisor Agent is shaping your allocation strategy…",
  "Debt Advisor Agent is assessing your loans & EMIs…",
  "Goal Planner Agent is mapping your milestones…",
  "Chief Financial Advisor is consolidating the final report…",
];

let loadingInterval = null;

function startLoadingMessages() {
  let i = 0;
  loadingText.textContent = LOADING_MESSAGES[0];
  loadingInterval = setInterval(() => {
    i = (i + 1) % LOADING_MESSAGES.length;
    loadingText.textContent = LOADING_MESSAGES[i];
  }, 1800);
}

function stopLoadingMessages() {
  clearInterval(loadingInterval);
}

function showState(state) {
  [emptyState, loadingState, errorState, reportContent].forEach((el) => el.classList.add("hidden"));
  state.classList.remove("hidden");
}

/**
 * Minimal Markdown -> HTML converter covering the subset of Markdown
 * the AI agents actually produce: headings (##), bold (**), unordered
 * lists (-/*), ordered lists (1.), and paragraphs.
 */
function renderMarkdown(md) {
  const lines = md.split("\n");
  let html = "";
  let inUl = false;
  let inOl = false;

  const closeLists = () => {
    if (inUl) { html += "</ul>"; inUl = false; }
    if (inOl) { html += "</ol>"; inOl = false; }
  };

  const inlineFormat = (text) =>
    text
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.+?)\*/g, "<em>$1</em>");

  for (const rawLine of lines) {
    const line = rawLine.trim();

    if (!line) { closeLists(); continue; }

    if (line.startsWith("## ")) {
      closeLists();
      html += `<h2>${inlineFormat(line.slice(3))}</h2>`;
      continue;
    }
    if (line.startsWith("# ")) {
      closeLists();
      html += `<h2>${inlineFormat(line.slice(2))}</h2>`;
      continue;
    }

    if (/^[-*]\s+/.test(line)) {
      if (!inUl) { closeLists(); html += "<ul>"; inUl = true; }
      html += `<li>${inlineFormat(line.replace(/^[-*]\s+/, ""))}</li>`;
      continue;
    }

    if (/^\d+\.\s+/.test(line)) {
      if (!inOl) { closeLists(); html += "<ol>"; inOl = true; }
      html += `<li>${inlineFormat(line.replace(/^\d+\.\s+/, ""))}</li>`;
      continue;
    }

    closeLists();
    html += `<p>${inlineFormat(line)}</p>`;
  }
  closeLists();
  return html;
}

/** Extracts the Financial Health Score (0-100) from the Chief report text. */
function extractScore(text) {
  const match = text.match(/Financial Health Score[:\s]*[\*_]*\s*(\d{1,3})\s*\/\s*100/i);
  if (match) {
    const val = parseInt(match[1], 10);
    return Math.max(0, Math.min(100, val));
  }
  return null;
}

function animateGauge(score) {
  const gauge = document.getElementById("score-gauge");
  const valueEl = document.getElementById("score-value");
  if (score === null) {
    valueEl.textContent = "N/A";
    gauge.style.setProperty("--score-percent", 0);
    return;
  }
  valueEl.textContent = score;
  // Animate via a short transition on the CSS custom property.
  requestAnimationFrame(() => {
    gauge.style.setProperty("--score-percent", score);
  });
}

function buildFullMarkdown(data) {
  return (
    `# FinPilot AI - Financial Report for ${data.name}\n` +
    `_Generated on ${data.generated_at}_\n\n` +
    `## Budget Analysis\n${data.budget_report}\n\n` +
    `## Investment Recommendations\n${data.investment_report}\n\n` +
    `## Debt Analysis\n${data.debt_report}\n\n` +
    `## Goal Planning\n${data.goal_report}\n\n` +
    `# Final Consolidated Report\n${data.final_report}\n`
  );
}

const aiProviderSelect = document.getElementById("ai_provider");
const apiKeyInput = document.getElementById("api_key");
const apiKeyHelp = document.getElementById("api_key_help");

const providerDetails = {
  groq: { placeholder: "gsk_...", text: 'Get a free API key at <a href="https://console.groq.com/keys" target="_blank">console.groq.com</a>.' },
  openai: { placeholder: "sk-...", text: 'Get an API key at <a href="https://platform.openai.com/api-keys" target="_blank">platform.openai.com</a>.' },
  gemini: { placeholder: "AIza...", text: 'Get an API key at <a href="https://aistudio.google.com/app/apikey" target="_blank">aistudio.google.com</a>.' },
  anthropic: { placeholder: "sk-ant-...", text: 'Get an API key at <a href="https://console.anthropic.com/settings/keys" target="_blank">console.anthropic.com</a>.' },
  openrouter: { placeholder: "sk-or-v1-...", text: 'Get an API key at <a href="https://openrouter.ai/keys" target="_blank">openrouter.ai</a>.' }
};

if(aiProviderSelect) {
  aiProviderSelect.addEventListener("change", (e) => {
    const details = providerDetails[e.target.value];
    if(details) {
      apiKeyInput.placeholder = details.placeholder;
      apiKeyHelp.innerHTML = details.text;
    }
  });
}

const checkKeyBtn = document.getElementById("check-key-btn");
const apiKeyStatus = document.getElementById("api_key_status");

if (checkKeyBtn) {
  checkKeyBtn.addEventListener("click", async () => {
    const provider = aiProviderSelect.value;
    const key = apiKeyInput.value.trim();
    if (!key) {
      apiKeyStatus.style.display = "block";
      apiKeyStatus.style.color = "red";
      apiKeyStatus.textContent = "Please enter an API key first.";
      return;
    }

    checkKeyBtn.disabled = true;
    checkKeyBtn.textContent = "Checking...";
    apiKeyStatus.style.display = "none";

    try {
      const response = await fetch("/api/validate-key", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ai_provider: provider, api_key: key })
      });
      const data = await response.json();
      
      apiKeyStatus.style.display = "block";
      if (response.ok && data.status === "valid") {
        apiKeyStatus.style.color = "green";
        apiKeyStatus.textContent = "✓ API Key is valid!";
      } else {
        apiKeyStatus.style.color = "red";
        apiKeyStatus.textContent = "✗ Invalid Key: " + (data.error || "Request failed");
      }
    } catch (err) {
      apiKeyStatus.style.display = "block";
      apiKeyStatus.style.color = "red";
      apiKeyStatus.textContent = "✗ Connection error.";
    } finally {
      checkKeyBtn.disabled = false;
      checkKeyBtn.textContent = "Check Key";
    }
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);
  const payload = {
    ai_provider: formData.get("ai_provider"),
    api_key: formData.get("api_key"),
    name: formData.get("name"),
    age: parseInt(formData.get("age"), 10),
    monthly_income: parseFloat(formData.get("monthly_income")),
    monthly_expenses: parseFloat(formData.get("monthly_expenses")),
    current_savings: parseFloat(formData.get("current_savings")),
    existing_investments: parseFloat(formData.get("existing_investments")),
    total_loan: parseFloat(formData.get("total_loan")),
    monthly_emi: parseFloat(formData.get("monthly_emi")),
    financial_goal: formData.get("financial_goal"),
    risk_preference: formData.get("risk_preference"),
  };

  submitBtn.disabled = true;
  showState(loadingState);
  startLoadingMessages();

  try {
    const response = await fetch("/api/generate-report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "The server returned an unexpected error.");
    }

    // Populate header
    document.getElementById("report-name").textContent = `${data.name}'s Financial Report`;
    document.getElementById("report-date").textContent = `Generated ${data.generated_at}`;

    // Populate score gauge
    const score = extractScore(data.final_report);
    animateGauge(score);

    // Populate consolidated report + individual agent sections
    document.getElementById("final-report-body").innerHTML = renderMarkdown(data.final_report);
    document.getElementById("budget-body").innerHTML = renderMarkdown(data.budget_report);
    document.getElementById("investment-body").innerHTML = renderMarkdown(data.investment_report);
    document.getElementById("debt-body").innerHTML = renderMarkdown(data.debt_report);
    document.getElementById("goal-body").innerHTML = renderMarkdown(data.goal_report);

    lastReportMarkdown = buildFullMarkdown(data);

    stopLoadingMessages();
    showState(reportContent);
  } catch (err) {
    stopLoadingMessages();
    errorText.textContent = err.message || "Something went wrong while generating your report.";
    showState(errorState);
  } finally {
    submitBtn.disabled = false;
  }
});

// ---- Copy report button ----
document.getElementById("copy-btn").addEventListener("click", async () => {
  if (!lastReportMarkdown) return;
  try {
    await navigator.clipboard.writeText(lastReportMarkdown);
    const btn = document.getElementById("copy-btn");
    const original = btn.textContent;
    btn.textContent = "Copied!";
    setTimeout(() => { btn.textContent = original; }, 1600);
  } catch {
    alert("Could not copy to clipboard. Please select and copy manually.");
  }
});

// ---- Download report as Markdown ----
document.getElementById("download-btn").addEventListener("click", () => {
  if (!lastReportMarkdown) return;
  const blob = new Blob([lastReportMarkdown], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "FinPilot_AI_Report.md";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
});
