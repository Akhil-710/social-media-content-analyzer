import re
from typing import Optional


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.
    Removes extra whitespace, handles encoding issues.

    Args:
        text (str): Raw extracted text

    Returns:
        str: Cleaned text
    """
    if not text:
        return ""

    # Remove extra whitespace (multiple spaces, tabs)
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    # Fix common OCR errors (optional, can be enhanced)
    text = _fix_ocr_errors(text)

    # Normalize line breaks
    text = text.replace('\r\n', '\n')

    return text


def _fix_ocr_errors(text: str) -> str:
    """
    Fix common OCR errors and encoding issues.

    Args:
        text (str): Text potentially containing OCR errors

    Returns:
        str: Corrected text
    """
    # Fix common OCR errors (these are examples, can be expanded)
    replacements = {
        '0': 'O',  # Zero to O (if in context)
        'l': 'I',  # Lowercase l to I (if in context)
        '|': 'I',  # Pipe to I (if in context)
    }

    # Note: We won't apply these blindly as they can cause issues
    # Instead, we just normalize unicode and handle encoding

    # Remove any null bytes or invalid characters
    text = text.encode('utf-8', errors='ignore').decode('utf-8')

    return text


def truncate_text(text: str, max_length: int = 1000) -> str:
    """
    Truncate text to maximum length.

    Args:
        text (str): Text to truncate
        max_length (int): Maximum length

    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."


def extract_sentences(text: str) -> list:
    """
    Extract sentences from text.

    Args:
        text (str): Input text

    Returns:
        list: List of sentences
    """
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def extract_paragraphs(text: str) -> list:
    """
    Extract paragraphs from text.

    Args:
        text (str): Input text

    Returns:
        list: List of paragraphs
    """
    paragraphs = text.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]


def remove_html_tags(text: str) -> str:
    """
    Remove HTML tags from text.

    Args:
        text (str): Text potentially containing HTML

    Returns:
        str: Text without HTML tags
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def remove_urls(text: str) -> str:
    """
    Remove URLs from text.

    Args:
        text (str): Text potentially containing URLs

    Returns:
        str: Text without URLs
    """
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)


def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
    """
    Remove special characters from text.

    Args:
        text (str): Input text
        keep_punctuation (bool): Whether to keep punctuation marks

    Returns:
        str: Cleaned text
    """
    if keep_punctuation:
        # Keep letters, numbers, spaces, and basic punctuation
        return re.sub(r'[^a-zA-Z0-9\s.!?,;:\'"@#\-]', '', text)
    else:
        # Keep only letters, numbers, and spaces
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)