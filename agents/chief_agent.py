"""
chief_agent.py

Chief Financial Advisor Agent - consolidates the outputs of the four
specialist agents into one final report, complete with a Financial
Health Score and top actionable recommendations.
"""

from agents.groq_client import call_llm
from prompts import CHIEF_AGENT_PROMPT, COMMON_STYLE_GUIDE


def run(profile: dict, budget_report: str, investment_report: str,
         debt_report: str, goal_report: str) -> str:
    """
    Builds the consolidation prompt using the user's profile plus the
    Markdown outputs of the four specialist agents, and returns the
    Chief Advisor's final Markdown report.
    """
    prompt = CHIEF_AGENT_PROMPT.format(
        name=profile["name"],
        age=profile["age"],
        monthly_income=profile["monthly_income"],
        monthly_expenses=profile["monthly_expenses"],
        current_savings=profile["current_savings"],
        existing_investments=profile["existing_investments"],
        total_loan=profile["total_loan"],
        monthly_emi=profile["monthly_emi"],
        financial_goal=profile["financial_goal"],
        risk_preference=profile["risk_preference"],
        budget_report=budget_report,
        investment_report=investment_report,
        debt_report=debt_report,
        goal_report=goal_report,
        style_guide=COMMON_STYLE_GUIDE,
    )
    # Chief report is longer (it consolidates everything), so allow more tokens.
    return call_llm(prompt, api_key=profile.get("api_key"), temperature=0.4, max_tokens=1100)
