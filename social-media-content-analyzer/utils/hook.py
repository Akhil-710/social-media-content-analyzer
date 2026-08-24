# ==========================================================================
# Hook Analysis Utility
# ==========================================================================

import re


def analyze_hook(text: str) -> int:
    """
    Calculate a simple hook effectiveness score from 0-100.
    """

    if not text or not text.strip():
        return 0

    text = text.strip()

    # Get the first sentence/line
    first_part = re.split(r"[.!?\n]", text)[0].strip()

    if not first_part:
        return 0

    score = 40

    # Questions can encourage curiosity
    if "?" in text[:150]:
        score += 20

    # Numbers/statistics can make hooks stronger
    if re.search(r"\b\d+[%+]?\b", first_part):
        score += 15

    # Strong attention-grabbing words
    strong_words = [
        "how",
        "why",
        "secret",
        "important",
        "discover",
        "learn",
        "mistake",
        "tips",
        "best",
        "warning",
        "new",
        "never",
        "stop",
        "start",
    ]

    first_lower = first_part.lower()

    for word in strong_words:
        if word in first_lower:
            score += 5
            break

    # Very short hook
    if len(first_part.split()) < 4:
        score -= 10

    return max(0, min(100, score))
    