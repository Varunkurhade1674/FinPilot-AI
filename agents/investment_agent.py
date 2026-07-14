"""
investment_agent.py

Investment Advisor Agent - analyzes risk profile and recommends an
investment allocation strategy.
"""

from agents.llm_client import call_llm
from prompts import INVESTMENT_AGENT_PROMPT, COMMON_STYLE_GUIDE


def run(profile: dict) -> str:
    """
    Builds the investment analysis prompt from the user's profile and
    returns the agent's Markdown response.
    """
    prompt = INVESTMENT_AGENT_PROMPT.format(
        name=profile["name"],
        age=profile["age"],
        current_savings=profile["current_savings"],
        existing_investments=profile["existing_investments"],
        financial_goal=profile["financial_goal"],
        risk_preference=profile["risk_preference"],
        style_guide=COMMON_STYLE_GUIDE,
    )
    return call_llm(prompt, ai_provider=profile.get("ai_provider", "groq"), api_key=profile.get("api_key"))
