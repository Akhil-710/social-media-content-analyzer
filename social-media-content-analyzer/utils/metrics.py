# ==========================================================================
# Content Metrics Utility
# Calculates basic text statistics and metrics
# ==========================================================================

import re
from typing import Dict


def calculate_metrics(text: str) -> Dict:
    """
    Calculate basic metrics from the provided text.

    Args:
        text (str): Text to analyze

    Returns:
        dict: Dictionary containing calculated metrics
    """

    if not text or not text.strip():
        return _get_empty_metrics()

    # Clean text
    text = text.strip()

    # ----------------------------------------------------------------------
    # WORDS
    # ----------------------------------------------------------------------

    words = re.findall(r"\b[\w']+\b", text)
    word_count = len(words)

    # ----------------------------------------------------------------------
    # CHARACTERS
    # ----------------------------------------------------------------------

    # Count all characters including spaces
    character_count = len(text)

    # Count characters excluding whitespace
    character_count_no_spaces = len(
        re.sub(r"\s+", "", text)
    )

    # ----------------------------------------------------------------------
    # SENTENCES
    # ----------------------------------------------------------------------

    # Split sentences using ., ! or ?
    sentences = re.split(r"[.!?]+", text)

    # Remove empty sentences
    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    sentence_count = len(sentences)

    # ----------------------------------------------------------------------
    # PARAGRAPHS
    # ----------------------------------------------------------------------

    paragraphs = re.split(r"\n\s*\n", text)

    paragraphs = [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]

    paragraph_count = len(paragraphs)

    # ----------------------------------------------------------------------
    # AVERAGE SENTENCE LENGTH
    # ----------------------------------------------------------------------

    if sentence_count > 0:
        avg_sentence_length = round(
            word_count / sentence_count,
            2
        )
    else:
        avg_sentence_length = 0

    # ----------------------------------------------------------------------
    # AVERAGE WORD LENGTH
    # ----------------------------------------------------------------------

    if word_count > 0:
        total_word_characters = sum(
            len(word)
            for word in words
        )

        avg_word_length = round(
            total_word_characters / word_count,
            2
        )
    else:
        avg_word_length = 0

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
    # SYLLABLE ESTIMATION
    # ----------------------------------------------------------------------

    syllable_count = _estimate_syllables(words)

    # ----------------------------------------------------------------------
    # RETURN ALL METRICS
    # ----------------------------------------------------------------------

    return {
        "word_count": word_count,
        "character_count": character_count,
        "character_count_no_spaces": character_count_no_spaces,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "avg_sentence_length": avg_sentence_length,
        "avg_word_length": avg_word_length,
        "hashtag_count": hashtag_count,
        "mention_count": mention_count,
        "question_count": question_count,
        "exclamation_count": exclamation_count,
        "emoji_count": emoji_count,
        "syllable_count": syllable_count,
    }


def _count_emojis(text: str) -> int:
    """
    Estimate the number of emojis in text.

    This uses Unicode ranges commonly associated with emojis.

    Args:
        text (str): Text to analyze

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

    return len(emoji_pattern.findall(text))


def _estimate_syllables(words: list) -> int:
    """
    Estimate the number of syllables in a list of words.

    This is a lightweight estimation and is not intended
    to replace a linguistic syllable library.

    Args:
        words (list): List of words

    Returns:
        int: Estimated syllable count
    """

    total_syllables = 0

    for word in words:
        word = re.sub(
            r"[^a-zA-Z]",
            "",
            word
        ).lower()

        if not word:
            continue

        # One syllable minimum
        syllables = 1

        # Count groups of vowels
        vowel_groups = re.findall(
            r"[aeiouy]+",
            word
        )

        syllables = len(vowel_groups)

        # Silent 'e' at the end
        if (
            word.endswith("e")
            and len(word) > 2
            and syllables > 1
        ):
            syllables -= 1

        # Words ending with "le"
        if (
            word.endswith("le")
            and len(word) > 2
            and word[-3] not in "aeiou"
        ):
            syllables += 1

        syllables = max(1, syllables)

        total_syllables += syllables

    return total_syllables


def _get_empty_metrics() -> Dict:
    """
    Return default metrics for empty text.

    Returns:
        dict: Empty metrics structure
    """

    return {
        "word_count": 0,
        "character_count": 0,
        "character_count_no_spaces": 0,
        "sentence_count": 0,
        "paragraph_count": 0,
        "avg_sentence_length": 0,
        "avg_word_length": 0,
        "hashtag_count": 0,
        "mention_count": 0,
        "question_count": 0,
        "exclamation_count": 0,
        "emoji_count": 0,
        "syllable_count": 0,
    }
    