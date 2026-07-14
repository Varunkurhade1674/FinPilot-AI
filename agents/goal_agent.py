"""
goal_agent.py

Goal Planner Agent - analyzes the user's stated financial goal and
generates a savings target with a milestone plan.
"""

from agents.llm_client import call_llm
from prompts import GOAL_AGENT_PROMPT, COMMON_STYLE_GUIDE


def run(profile: dict) -> str:
    """
    Builds the goal planning prompt from the user's profile and
    returns the agent's Markdown response.
    """
    prompt = GOAL_AGENT_PROMPT.format(
        name=profile["name"],
        age=profile["age"],
        monthly_income=profile["monthly_income"],
        monthly_expenses=profile["monthly_expenses"],
        current_savings=profile["current_savings"],
        financial_goal=profile["financial_goal"],
        style_guide=COMMON_STYLE_GUIDE,
    )
    return call_llm(prompt, ai_provider=profile.get("ai_provider", "groq"), api_key=profile.get("api_key"))
