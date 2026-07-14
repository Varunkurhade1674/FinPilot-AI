# FinPilot AI — Multi-Agent Financial Advisor

FinPilot AI is a production-ready, highly aesthetic web application where **five collaborating AI agents** analyze a user's financial profile and produce a personalized, consolidated financial plan. It is built entirely on **FastAPI**, **Jinja2**, and vanilla **HTML/CSS/JS**, featuring a stunning **Dynamic Vibrant UI** with playful animations and glassmorphism panels.

It features **multi-LLM support**, allowing you to seamlessly switch between **Groq**, **OpenAI**, **Google Gemini**, **Anthropic**, and **OpenRouter** directly from the dashboard!

No database, no auth, no external financial APIs, no deployment tooling — just a beautiful, clean multi-agent pipeline you can run locally in minutes.

---

## 🚀 Features

- 🧠 **Multi-Agent Pipeline**: 5 specialized AI agents, each with its own reusable prompt template.
- ⚡ **Concurrent Execution**: Specialist agents run concurrently (via `asyncio.gather` + threads) for blazing fast analysis.
- 🤖 **Bring Your Own AI**: Built-in support for Groq (Llama 3.3), OpenAI (GPT-4o), Google Gemini (1.5), Anthropic (Claude 3.5), and OpenRouter. Switch effortlessly via a dropdown.
- 🔑 **Live Key Validation**: Verify your API keys instantly from the UI with an embedded check button.
- 🎨 **Dynamic Vibrant UI**: A radically modern, eye-catching interface featuring an animated gradient background, frosted glass panels, pill buttons, and responsive spring animations.
- 📊 **Animated Health Score**: Beautiful dynamic gauge (0–100) that physically counts up.
- 📝 **Export Options**: Copy your consolidated final report to the clipboard or download it directly as a `.md` Markdown file. Auto-saves to the `reports/` directory.
- 🎯 **Clean Error Handling**: Invalid API keys or connection errors show friendly inline alerts.

---

## 🏗️ Agent Workflow

```text
                     ┌─────────────────────┐
                     │   User Financial    │
                     │       Profile       │
                     └──────────┬──────────┘
                                │
          ┌─────────────┬───────┼────────┬─────────────┐
          ▼             ▼       ▼        ▼             ▼
   ┌─────────────┐┌──────────┐┌────────┐┌────────────┐
   │   Budget    ││Investment││  Debt  ││    Goal    │  (run concurrently)
   │   Planner   ││ Advisor  ││Advisor ││  Planner   │
   └──────┬──────┘└────┬─────┘└───┬────┘└──────┬─────┘
          │            │          │            │
          └────────────┴────┬─────┴────────────┘
                            ▼
                 ┌───────────────────────┐
                 │  Chief Financial      │
                 │  Advisor (synthesis)  │
                 │  → Health Score       │
                 │  → Top 5 Actions      │
                 │  → Final Report       │
                 └───────────────────────┘
```

Each specialist agent calls your selected LLM API independently. The **Chief Financial Advisor** agent receives the user's raw profile *plus* all four specialist outputs, and synthesizes them into the final actionable Markdown report.

---

## 📂 Folder Structure

```text
FinPilot-AI/
│
├── agents/
│   ├── __init__.py
│   ├── llm_client.py        # Generic LLM router (Groq, OpenAI, Gemini, Anthropic)
│   ├── budget_agent.py      # Budget Planner Agent
│   ├── investment_agent.py  # Investment Advisor Agent
│   ├── debt_agent.py        # Debt Advisor Agent
│   ├── goal_agent.py        # Goal Planner Agent
│   └── chief_agent.py       # Chief Financial Advisor Agent
│
├── templates/
│   └── index.html           # Dynamic Vibrant Dashboard (form + report panel)
│
├── static/
│   ├── style.css            # Stunning gradient/glassmorphism design system
│   └── script.js            # UI interactions, API Key validation, Markdown rendering
│
├── reports/                 # Auto-saved Markdown reports (gitignored)
│
├── app.py                   # FastAPI backend & endpoints
├── prompts.py               # Prompt engineering templates for each agent
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer          | Technology                          |
|----------------|--------------------------------------|
| Backend        | Python 3.10+, FastAPI, Uvicorn       |
| Templating     | Jinja2                               |
| Frontend       | HTML5, CSS3 (Custom Properties), vanilla JS |
| AI / LLM       | SDKs: `openai`, `google-genai`, `anthropic`, `groq` |
| Validation     | Pydantic                             |

---

## ⚡ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Varunkurhade1674/FinPilot-AI.git
   cd FinPilot-AI
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables (Optional but recommended)**
   
   If you want the API keys to be automatically detected instead of typing them into the UI, create a `.env` file and add your keys:
   ```bash
   GROQ_API_KEY=your_groq_key
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   ANTHROPIC_API_KEY=your_anthropic_key
   OPENROUTER_API_KEY=your_openrouter_key
   ```
   *Note: You can always just paste your key directly into the web UI when using the app.*

---

## 🚀 Running the Application

Start the FastAPI server:

```bash
python app.py
```

Then open your browser at:
**[http://localhost:8000](http://localhost:8000)**

---

## 💡 Example Usage

1. **Select your AI**: Use the dropdown in the UI to select your preferred AI Provider (e.g., Groq, OpenAI).
2. **Verify your Key**: Paste your API key into the field and click the **Verify** button embedded in the input box to ensure it's valid.
3. **Fill your Profile**: Enter your income, expenses, savings, investments, loan amount, EMI, financial goal, and risk preference.
4. **Generate**: Click **Generate Financial Report**.
5. **Watch the Magic**: See the gorgeous shimmering loader as each agent runs.
6. **Review & Export**: Review your **Financial Health Score** (watch the counter animation!), read the consolidated report, and use the **Download .md** button to save it locally.

---

## 📝 Notes

- This project intentionally avoids a database and authentication to stay lightweight and fast to run.
- All financial figures are treated as illustrative user input — this is a planning/advisory tool, not real-time financial market advice.
