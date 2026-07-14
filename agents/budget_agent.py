"""
budget_agent.py

Budget Planner Agent - analyzes income vs expenses and recommends
a savings target and budgeting improvements.
"""

from agents.groq_client import call_llm
from prompts import BUDGET_AGENT_PROMPT, COMMON_STYLE_GUIDE


def run(profile: dict) -> str:
    """
    Builds the budget analysis prompt from the user's profile and
    returns the agent's Markdown response.
    """
    prompt = BUDGET_AGENT_PROMPT.format(
        name=profile["name"],
        monthly_income=profile["monthly_income"],
        monthly_expenses=profile["monthly_expenses"],
        current_savings=profile["current_savings"],
        style_guide=COMMON_STYLE_GUIDE,
    )
    return call_llm(prompt, api_key=profile.get("api_key"))
