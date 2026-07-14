"""
app.py

FinPilot AI - Multi-Agent Financial Advisor
Main FastAPI application entry point.

Serves the dashboard UI and exposes a single API endpoint that runs
all five AI agents (Budget, Investment, Debt, Goal, Chief) against a
user-submitted financial profile and returns a consolidated report.
"""

import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from agents import budget_agent, investment_agent, debt_agent, goal_agent, chief_agent

# Load environment variables (GROQ_API_KEY) from .env
load_dotenv()

app = FastAPI(title="FinPilot AI - Multi-Agent Financial Advisor")

# Static files (CSS/JS) and Jinja2 templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


class FinancialProfile(BaseModel):
    """Schema for the financial profile submitted by the user."""

    name: str = Field(..., min_length=1)
    age: int = Field(..., gt=0, lt=120)
    monthly_income: float = Field(..., ge=0)
    monthly_expenses: float = Field(..., ge=0)
    current_savings: float = Field(..., ge=0)
    existing_investments: float = Field(..., ge=0)
    total_loan: float = Field(..., ge=0)
    monthly_emi: float = Field(..., ge=0)
    financial_goal: str = Field(..., min_length=1)
    risk_preference: str = Field(..., pattern="^(Low|Medium|High)$")
    ai_provider: str = Field(default="groq")
    api_key: str = Field(default="")


@app.get("/")
async def home(request: Request):
    """Renders the main dashboard page."""
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/api/generate-report")
async def generate_report(profile: FinancialProfile):
    """
    Runs all five AI agents against the submitted financial profile and
    returns each agent's analysis plus the consolidated final report.
    """
    profile_dict = profile.model_dump()

    try:
        # Run the four specialist agents concurrently in worker threads,
        # since the Groq SDK call is blocking/synchronous.
        budget_report, investment_report, debt_report, goal_report = await asyncio.gather(
            asyncio.to_thread(budget_agent.run, profile_dict),
            asyncio.to_thread(investment_agent.run, profile_dict),
            asyncio.to_thread(debt_agent.run, profile_dict),
            asyncio.to_thread(goal_agent.run, profile_dict),
        )

        # Chief Advisor consolidates the four specialist reports.
        final_report = await asyncio.to_thread(
            chief_agent.run,
            profile_dict,
            budget_report,
            investment_report,
            debt_report,
            goal_report,
        )

    except RuntimeError as exc:
        # Surfaces a clean, readable error (e.g. missing/invalid API key)
        return JSONResponse(status_code=500, content={"error": str(exc)})

    result = {
        "name": profile.name,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "budget_report": budget_report,
        "investment_report": investment_report,
        "debt_report": debt_report,
        "goal_report": goal_report,
        "final_report": final_report,
    }

    # Persist a Markdown copy of the report to disk for record-keeping.
    _save_report_to_disk(result)

    return JSONResponse(content=result)


def _save_report_to_disk(result: dict) -> None:
    """
    Writes a full Markdown version of the generated report into the
    reports/ directory, named with the user's name and a timestamp.
    """
    safe_name = "".join(c for c in result["name"] if c.isalnum() or c in (" ", "_")).strip()
    safe_name = safe_name.replace(" ", "_") or "user"
    filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join(REPORTS_DIR, filename)

    content = (
        f"# FinPilot AI - Financial Report for {result['name']}\n"
        f"_Generated on {result['generated_at']}_\n\n"
        f"## Budget Analysis\n{result['budget_report']}\n\n"
        f"## Investment Recommendations\n{result['investment_report']}\n\n"
        f"## Debt Analysis\n{result['debt_report']}\n\n"
        f"## Goal Planning\n{result['goal_report']}\n\n"
        f"# Final Consolidated Report\n{result['final_report']}\n"
    )

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError:
        # Non-fatal: if disk write fails, the user still gets the report in the UI.
        pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
