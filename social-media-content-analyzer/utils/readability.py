# ==========================================================================
# Readability Analysis Utility
# Calculates a simple readability score for social media content
# ==========================================================================

from typing import Dict


def calculate_readability_score(text: str, metrics: Dict) -> int:
    """
    Calculate a readability score from 0-100.

    The score is a heuristic designed for this application.
    It considers:
    - Average sentence length
    - Average word length
    - Sentence count
    - Word count

    Higher score = easier to read.

    Args:
        text (str): Original text
        metrics (dict): Metrics calculated by calculate_metrics()

    Returns:
        int: Readability score from 0 to 100
    """

    if not text or not text.strip():
        return 0

    word_count = metrics.get("word_count", 0)
    sentence_count = metrics.get("sentence_count", 0)
    avg_sentence_length = metrics.get(
        "avg_sentence_length",
        0
    )
    avg_word_length = metrics.get(
        "avg_word_length",
        0
    )

    if word_count == 0:
        return 0

    # ----------------------------------------------------------------------
    # BASE SCORE
    # ----------------------------------------------------------------------

    score = 100

    # ----------------------------------------------------------------------
    # SENTENCE LENGTH
    # ----------------------------------------------------------------------
    # Social media content is generally easier to read when sentences
    # are reasonably short.

    if avg_sentence_length <= 12:
        sentence_penalty = 0

    elif avg_sentence_length <= 18:
        sentence_penalty = 5

    elif avg_sentence_length <= 25:
        sentence_penalty = 15

    elif avg_sentence_length <= 35:
        sentence_penalty = 25

    else:
        sentence_penalty = 35

    score -= sentence_penalty

    # ----------------------------------------------------------------------
    # WORD LENGTH
    # ----------------------------------------------------------------------

    if avg_word_length <= 5:
        word_penalty = 0

    elif avg_word_length <= 6:
        word_penalty = 5

    elif avg_word_length <= 7:
        word_penalty = 10

    elif avg_word_length <= 8:
        word_penalty = 15

    else:
        word_penalty = 20

    score -= word_penalty

    # ----------------------------------------------------------------------
    # VERY SHORT CONTENT
    # ----------------------------------------------------------------------

    if word_count < 10:
        score -= 10

    # ----------------------------------------------------------------------
    # NO SENTENCES DETECTED
    # ----------------------------------------------------------------------

    if sentence_count == 0:
        score -= 20

    # ----------------------------------------------------------------------
    # FINAL SCORE
    # ----------------------------------------------------------------------

    return max(0, min(100, int(score)))


def get_readability_label(score: int) -> str:
    """
    Convert readability score into a human-readable label.

    Args:
        score (int): Readability score from 0-100

    Returns:
        str: Readability category
    """

    if score >= 90:
        return "Very Easy"

    elif score >= 80:
        return "Easy"

    elif score >= 70:
        return "Good"

    elif score >= 60:
        return "Moderate"

    elif score >= 50:
        return "Difficult"

    else:
        return "Very Difficult"


def get_readability_advice(score: int) -> str:
    """
    Generate basic readability advice based on the score.

    Args:
        score (int): Readability score

    Returns:
        str: Advice message
    """

    if score >= 80:
        return (
            "Your content is easy to read and should be "
            "accessible to most audiences."
        )

    elif score >= 60:
        return (
            "Your content has reasonable readability, "
            "but some sentences could be simplified."
        )

    elif score >= 40:
        return (
            "Consider using shorter sentences and simpler "
            "words to improve readability."
        )

    else:
        return (
            "Your content may be difficult to read. "
            "Use shorter sentences and simpler language."
        )
        