"""Human escalation agent."""

def human_response(question: str) -> str:
    """Fallback response when review is required."""
    return f"Further review required for question: {question}"
