"""
debt_agent.py

Debt Advisor Agent - analyzes loans/EMIs and recommends a repayment
and debt reduction strategy.
"""

from agents.groq_client import call_llm
from prompts import DEBT_AGENT_PROMPT, COMMON_STYLE_GUIDE


def run(profile: dict) -> str:
    """
    Builds the debt analysis prompt from the user's profile and
    returns the agent's Markdown response.
    """
    prompt = DEBT_AGENT_PROMPT.format(
        name=profile["name"],
        monthly_income=profile["monthly_income"],
        total_loan=profile["total_loan"],
        monthly_emi=profile["monthly_emi"],
        style_guide=COMMON_STYLE_GUIDE,
    )
    return call_llm(prompt, api_key=profile.get("api_key"))
