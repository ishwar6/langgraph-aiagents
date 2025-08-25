"""Proxy for human review when automated confidence is low."""

def human_response(question: str) -> str:
    """Return a message requesting manual inspection.

    Parameters
    ----------
    question: str
        Original query that needs review.

    Returns
    -------
    str
        Notice that a human should provide the final answer.
    """
    return f"Further review required for question: {question}"
