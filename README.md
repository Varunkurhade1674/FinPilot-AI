# FinPilot AI — Multi-Agent Financial Advisor

FinPilot AI is a compact, production-ready web application where **five
collaborating AI agents** analyze a user's financial profile and produce a
personalized, consolidated financial plan — built entirely on **FastAPI**,
**Jinja2**, vanilla **HTML/CSS/JS**, and the **Groq API (Llama 3.3)**.

No database, no auth, no external financial APIs, no deployment tooling —
just a clean multi-agent pipeline you can run locally in minutes.

---

## Project Overview

A user fills out a single financial profile form (income, expenses, savings,
investments, loans, goals, and risk preference). That profile is sent to a
pipeline of five specialized AI agents:

1. **Budget Planner Agent** — analyzes income vs. expenses and recommends a savings target.
2. **Investment Advisor Agent** — analyzes risk profile and recommends an asset allocation.
3. **Debt Advisor Agent** — analyzes loans/EMIs and recommends a repayment strategy.
4. **Goal Planner Agent** — turns a stated financial goal into a savings target and milestones.
5. **Chief Financial Advisor** — consolidates all four reports into one final report, complete
   with a **Financial Health Score (0–100)** and a **Top 5 Actionable Recommendations** list.

The result is rendered in a two-panel dashboard: inputs on the left, the
generated report (with a live score gauge) on the right.

---

## Features

- 🧠 5 specialized AI agents, each with its own reusable prompt template
- ⚡ Specialist agents run **concurrently** (via `asyncio.gather` + threads) for speed
- 📊 Animated **Financial Health Score** gauge (0–100)
- 📝 Consolidated final report + collapsible per-agent detail sections
- 📋 **Copy Report** button (clipboard) and **Download as Markdown** button
- 💾 Every generated report is also auto-saved to `reports/` as a `.md` file
- 🎯 Clean error handling — a missing/invalid Groq API key shows a friendly message instead of a crash
- 📱 Fully responsive layout (desktop → tablet → mobile)
- 🚫 No React, no database, no auth, no Docker, no paid UI libraries

---

## Agent Workflow

```
                     ┌─────────────────────┐
                     │   User Financial     │
                     │       Profile        │
                     └──────────┬───────────┘
                                │
          ┌─────────────┬───────┼────────┬─────────────┐
          ▼             ▼       ▼         ▼             ▼
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

Each specialist agent calls the Groq API independently with its own focused
prompt (see `prompts.py`). The Chief Financial Advisor agent receives the
user's raw profile *plus* all four specialist outputs, and produces the
final synthesized Markdown report shown in the UI.

---

## Folder Structure

```
FinPilot-AI/
│
├── agents/
│   ├── __init__.py
│   ├── groq_client.py       # Shared Groq API wrapper used by every agent
│   ├── budget_agent.py      # Budget Planner Agent
│   ├── investment_agent.py  # Investment Advisor Agent
│   ├── debt_agent.py        # Debt Advisor Agent
│   ├── goal_agent.py        # Goal Planner Agent
│   └── chief_agent.py       # Chief Financial Advisor Agent
│
├── templates/
│   └── index.html           # Dashboard (form + report panel)
│
├── static/
│   ├── style.css            # Design system + responsive layout
│   └── script.js            # Form handling, Markdown rendering, score gauge
│
├── reports/                 # Auto-saved Markdown reports (gitignored)
│
├── app.py                   # FastAPI application & API endpoint
├── prompts.py                # All agent prompt templates
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Tech Stack

| Layer          | Technology                          |
|----------------|--------------------------------------|
| Backend        | Python 3.10+, FastAPI, Uvicorn       |
| Templating     | Jinja2                               |
| Frontend       | HTML5, CSS3, vanilla JavaScript      |
| AI / LLM       | Groq API — Llama 3.3 70B Versatile   |
| Config         | python-dotenv                        |
| Validation     | Pydantic                             |

---

## Installation

1. **Clone / copy the project**

   ```bash
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

4. **Configure your Groq API key**

   ```bash
   cp .env.example .env
   ```

   Then open `.env` and set:

   ```
   GROQ_API_KEY=your_real_groq_api_key
   ```

   You can get a free key at [console.groq.com/keys](https://console.groq.com/keys).

---

## Running the Application

```bash
python app.py
```

or, equivalently:

```bash
uvicorn app:app --reload --port 8000
```

Then open your browser at:

```
http://localhost:8000
```

---

## Example Usage

1. Fill out the form on the left: name, age, income, expenses, savings,
   investments, loan amount, EMI, financial goal, and risk preference.
2. Click **Generate Financial Report**.
3. Watch the rotating status messages as each agent runs (Budget → Investment
   → Debt → Goal → Chief Advisor).
4. Review your **Financial Health Score**, the consolidated report, and the
   **Top 5 Actionable Recommendations**.
5. Expand any of the four collapsible sections to see each specialist
   agent's full analysis.
6. Use **Copy Report** to copy the full Markdown to your clipboard, or
   **Download .md** to save it locally. A copy is also automatically saved
   to the `reports/` folder on the server.

---

## Future Enhancements

- Multi-currency support and locale-aware number formatting
- Historical report comparison (track Financial Health Score over time)
- Export report as PDF in addition to Markdown
- Optional chat-style follow-up questions to each individual agent
- Streaming agent responses token-by-token instead of waiting for completion
- Configurable agent models (e.g. swap Llama 3.3 for another Groq-hosted model)

---

## Notes

- This project intentionally avoids a database, authentication, and
  external financial data providers to stay lightweight and fast to run.
- All financial figures are treated as illustrative user input — this is a
  planning/advisory tool, not a real-time market data or brokerage product.
