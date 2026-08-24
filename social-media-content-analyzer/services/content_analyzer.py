# ==========================================================================
# Content Analyzer Service
# Analyzes text content and calculates various metrics and scores
# ==========================================================================

import re
from typing import Dict, Any
from utils.metrics import calculate_metrics
from utils.engagement import analyze_engagement
from utils.readability import calculate_readability_score
from utils.hook import analyze_hook


class ContentAnalyzer:
    """
    Comprehensive content analysis service.
    Calculates metrics, engagement, readability, and hook effectiveness.
    """

    def __init__(self):
        """Initialize content analyzer."""
        pass

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on content.

        Args:
            text (str): The text content to analyze

        Returns:
            dict: Complete analysis results
        """
        try:
            # Calculate all metrics
            metrics = calculate_metrics(text)
            engagement = analyze_engagement(text)
            readability_score = calculate_readability_score(text, metrics)
            hook_score = analyze_hook(text)

            # Calculate overall score (weighted average)
            overall_score = int(
                (readability_score * 0.4) +
                (engagement['engagement_score'] * 0.3) +
                (hook_score * 0.3)
            )

            # Compile analysis results
            analysis = {
                'overall_score': overall_score,
                'engagement_score': engagement['engagement_score'],
                'readability_score': readability_score,
                'hook_score': hook_score,
                'metrics': {
                    'word_count': metrics['word_count'],
                    'character_count': metrics['character_count'],
                    'sentence_count': metrics['sentence_count'],
                    'paragraph_count': metrics['paragraph_count'],
                    'avg_sentence_length': metrics['avg_sentence_length'],
                    'avg_word_length': metrics['avg_word_length']
                },
                'engagement': {
                    'hashtag_count': engagement['hashtag_count'],
                    'mention_count': engagement['mention_count'],
                    'question_count': engagement['question_count'],
                    'exclamation_count': engagement['exclamation_count'],
                    'emoji_count': engagement.get('emoji_count', 0),
                    'cta_present': engagement['cta_present']
                },
                'readability_details': {
                    'flesch_kincaid_grade': self._calculate_flesch_kincaid(metrics),
                    'is_easy_to_read': readability_score >= 70
                }
            }

            return analysis

        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            return self._get_default_analysis()

    def _calculate_flesch_kincaid(self, metrics: Dict) -> float:
        """
        Calculate Flesch-Kincaid Grade Level.
        Formula: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59

        Args:
            metrics (dict): Metrics dictionary

        Returns:
            float: Grade level
        """
        try:
            words = metrics['word_count']
            sentences = metrics['sentence_count']
            syllables = metrics.get('syllable_count', words)  # Rough estimate

            if sentences == 0 or words == 0:
                return 0

            grade = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
            return max(0, min(18, grade))  # Clamp between 0-18

        except Exception as e:
            print(f"Error calculating Flesch-Kincaid: {str(e)}")
            return 0

    def get_score_interpretation(self, score: int) -> str:
        """
        Get human-readable interpretation of a score.

        Args:
            score (int): Score value (0-100)

        Returns:
            str: Interpretation
        """
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Very Good"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        elif score >= 50:
            return "Needs Improvement"
        else:
            return "Poor"

    def _get_default_analysis(self) -> Dict[str, Any]:
        """
        Get default/empty analysis structure.

        Returns:
            dict: Default analysis values
        """
        return {
            'overall_score': 0,
            'engagement_score': 0,
            'readability_score': 0,
            'hook_score': 0,
            'metrics': {
                'word_count': 0,
                'character_count': 0,
                'sentence_count': 0,
                'paragraph_count': 0,
                'avg_sentence_length': 0,
                'avg_word_length': 0
            },
            'engagement': {
                'hashtag_count': 0,
                'mention_count': 0,
                'question_count': 0,
                'exclamation_count': 0,
                'emoji_count': 0,
                'cta_present': False
            },
            'readability_details': {
                'flesch_kincaid_grade': 0,
                'is_easy_to_read': False
            }
        }
        