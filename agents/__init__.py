"""
agents package

Contains one module per AI agent. Each agent exposes a single
`run(profile: dict) -> str` function that builds a prompt from
prompts.py, calls the Groq LLM, and returns a Markdown string.
"""
