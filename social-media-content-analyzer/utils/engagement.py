# ==========================================================================
# Engagement Analysis Utility
# Detects engagement elements and calculates an engagement score
# ==========================================================================

import re
from typing import Dict


# Common Call-To-Action phrases
CTA_PHRASES = [
    "comment",
    "share",
    "follow",
    "subscribe",
    "learn more",
    "click here",
    "visit",
    "tell us",
    "let me know",
    "what do you think",
    "join us",
    "sign up",
    "check out",
    "download",
    "get started",
    "try now",
    "buy now",
    "shop now",
]


def analyze_engagement(text: str) -> Dict:
    """
    Analyze engagement-related elements in social media content.

    Args:
        text (str): Text content to analyze

    Returns:
        dict: Engagement metrics and score
    """

    if not text or not text.strip():
        return _get_empty_engagement()

    text = text.strip()

    # ----------------------------------------------------------------------
    # HASHTAGS
    # ----------------------------------------------------------------------

    hashtags = re.findall(
        r"(?<!\w)#\w+",
        text
    )

    hashtag_count = len(hashtags)

    # ----------------------------------------------------------------------
    # MENTIONS
    # ----------------------------------------------------------------------

    mentions = re.findall(
        r"(?<!\w)@\w+",
        text
    )

    mention_count = len(mentions)

    # ----------------------------------------------------------------------
    # QUESTIONS
    # ----------------------------------------------------------------------

    question_count = text.count("?")

    # ----------------------------------------------------------------------
    # EXCLAMATIONS
    # ----------------------------------------------------------------------

    exclamation_count = text.count("!")

    # ----------------------------------------------------------------------
    # EMOJIS
    # ----------------------------------------------------------------------

    emoji_count = _count_emojis(text)

    # ----------------------------------------------------------------------
    # CTA DETECTION
    # ----------------------------------------------------------------------

    cta_present, detected_ctas = _detect_cta(text)

    # ----------------------------------------------------------------------
    # ENGAGEMENT SCORE
    # ----------------------------------------------------------------------

    engagement_score = _calculate_engagement_score(
        hashtag_count=hashtag_count,
        mention_count=mention_count,
        question_count=question_count,
        exclamation_count=exclamation_count,
        emoji_count=emoji_count,
        cta_present=cta_present
    )

    return {
        "engagement_score": engagement_score,
        "hashtag_count": hashtag_count,
        "mention_count": mention_count,
        "question_count": question_count,
        "exclamation_count": exclamation_count,
        "emoji_count": emoji_count,
        "cta_present": cta_present,
        "detected_ctas": detected_ctas,
    }


def _detect_cta(text: str):
    """
    Detect common call-to-action phrases.

    Args:
        text (str): Text content

    Returns:
        tuple: (CTA present, detected CTA phrases)
    """

    text_lower = text.lower()

    detected_ctas = []

    for phrase in CTA_PHRASES:
        if phrase in text_lower:
            detected_ctas.append(phrase)

    return (
        len(detected_ctas) > 0,
        detected_ctas
    )


def _calculate_engagement_score(
    hashtag_count: int,
    mention_count: int,
    question_count: int,
    exclamation_count: int,
    emoji_count: int,
    cta_present: bool
) -> int:
    """
    Calculate a heuristic engagement score from 0-100.

    This is a rule-based heuristic and does not represent
    guaranteed real-world social media engagement.

    Args:
        hashtag_count: Number of hashtags
        mention_count: Number of mentions
        question_count: Number of questions
        exclamation_count: Number of exclamations
        emoji_count: Number of emojis
        cta_present: Whether a CTA was detected

    Returns:
        int: Engagement score from 0-100
    """

    score = 0

    # ----------------------------------------------------------------------
    # HASHTAGS - Maximum 20 points
    # ----------------------------------------------------------------------

    if 3 <= hashtag_count <= 8:
        score += 20
    elif 1 <= hashtag_count <= 2:
        score += 12
    elif 9 <= hashtag_count <= 12:
        score += 10
    elif hashtag_count > 12:
        score += 5

    # ----------------------------------------------------------------------
    # QUESTIONS - Maximum 20 points
    # ----------------------------------------------------------------------

    if question_count >= 1:
        score += 20

    # ----------------------------------------------------------------------
    # CTA - Maximum 25 points
    # ----------------------------------------------------------------------

    if cta_present:
        score += 25

    # ----------------------------------------------------------------------
    # MENTIONS - Maximum 15 points
    # ----------------------------------------------------------------------

    if 1 <= mention_count <= 5:
        score += 15
    elif mention_count > 5:
        score += 8

    # ----------------------------------------------------------------------
    # EMOJIS - Maximum 10 points
    # ----------------------------------------------------------------------

    if 1 <= emoji_count <= 5:
        score += 10
    elif emoji_count > 5:
        score += 5

    # ----------------------------------------------------------------------
    # EXCLAMATIONS - Maximum 10 points
    # ----------------------------------------------------------------------

    if 1 <= exclamation_count <= 3:
        score += 10
    elif exclamation_count > 3:
        score += 5

    # Keep score between 0 and 100
    return min(100, max(0, score))


def _count_emojis(text: str) -> int:
    """
    Count common Unicode emojis.

    Args:
        text (str): Text content

    Returns:
        int: Approximate emoji count
    """

    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001F5FF"
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FAFF"
        "\U00002700-\U000027BF"
        "\U00002600-\U000026FF"
        "]"
    )

    return len(
        emoji_pattern.findall(text)
    )


def _get_empty_engagement() -> Dict:
    """
    Return default engagement results for empty text.

    Returns:
        dict: Empty engagement structure
    """

    return {
        "engagement_score": 0,
        "hashtag_count": 0,
        "mention_count": 0,
        "question_count": 0,
        "exclamation_count": 0,
        "emoji_count": 0,
        "cta_present": False,
        "detected_ctas": [],
    }
    