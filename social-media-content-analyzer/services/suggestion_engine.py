# ==========================================================================
# Suggestion Engine Service
# Generates actionable suggestions based on content analysis
# ==========================================================================

from typing import List, Dict, Any


class SuggestionEngine:
    """
    Generates actionable suggestions based on content analysis results.
    """

    def __init__(self):
        """Initialize suggestion engine."""
        pass

    def generate(self, text: str, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate suggestions based on analysis results.

        Args:
            text (str): The original text content
            analysis (dict): Analysis results from ContentAnalyzer

        Returns:
            list: List of suggestion dictionaries with category and message
        """
        suggestions = []

        try:
            # Hook suggestions
            hook_suggestions = self._generate_hook_suggestions(analysis)
            suggestions.extend(hook_suggestions)

            # Engagement suggestions
            engagement_suggestions = self._generate_engagement_suggestions(analysis, text)
            suggestions.extend(engagement_suggestions)

            # Readability suggestions
            readability_suggestions = self._generate_readability_suggestions(analysis)
            suggestions.extend(readability_suggestions)

            # Length suggestions
            length_suggestions = self._generate_length_suggestions(analysis)
            suggestions.extend(length_suggestions)

            # If no suggestions, provide encouragement
            if not suggestions:
                suggestions.append({
                    'category': 'Excellent',
                    'message': 'Your content is well-optimized! Keep up the great work.'
                })

            return suggestions

        except Exception as e:
            print(f"Error generating suggestions: {str(e)}")
            return [{'category': 'Error', 'message': 'Could not generate suggestions'}]

    def _generate_hook_suggestions(self, analysis: Dict) -> List[Dict[str, str]]:
        """Generate hook-related suggestions."""
        suggestions = []
        hook_score = analysis.get('hook_score', 0)

        if hook_score < 50:
            suggestions.append({
                'category': 'Hook',
                'message': 'Start with a bold statement or question to grab attention immediately.'
            })
        elif hook_score < 70:
            suggestions.append({
                'category': 'Hook',
                'message': 'Try opening with a surprising fact or statistic to increase impact.'
            })

        return suggestions

    def _generate_engagement_suggestions(self, analysis: Dict, text: str) -> List[Dict[str, str]]:
        """Generate engagement-related suggestions."""
        suggestions = []
        engagement = analysis.get('engagement', {})
        engagement_score = analysis.get('engagement_score', 0)

        hashtag_count = engagement.get('hashtag_count', 0)
        mention_count = engagement.get('mention_count', 0)
        question_count = engagement.get('question_count', 0)
        cta_present = engagement.get('cta_present', False)

        # Hashtag suggestions
        if hashtag_count == 0:
            suggestions.append({
                'category': 'Engagement',
                'message': 'Add 3-5 relevant hashtags to increase discoverability on social media.'
            })
        elif hashtag_count > 10:
            suggestions.append({
                'category': 'Engagement',
                'message': f'You have {hashtag_count} hashtags. Consider reducing to 5-8 for better focus.'
            })

        # Question suggestions
        if question_count == 0:
            suggestions.append({
                'category': 'Engagement',
                'message': 'Include a question to encourage audience interaction and comments.'
            })

        # CTA suggestions
        if not cta_present:
            suggestions.append({
                'category': 'Engagement',
                'message': 'Add a clear Call-to-Action (CTA) like "Click here", "Learn more", or "Share your thoughts".'
            })

        # Mention suggestions
        if mention_count == 0 and len(text) > 100:
            suggestions.append({
                'category': 'Engagement',
                'message': 'Consider mentioning relevant people or brands to expand reach.'
            })

        return suggestions

    def _generate_readability_suggestions(self, analysis: Dict) -> List[Dict[str, str]]:
        """Generate readability-related suggestions."""
        suggestions = []
        readability_score = analysis.get('readability_score', 0)
        metrics = analysis.get('metrics', {})
        avg_sentence_length = metrics.get('avg_sentence_length', 0)

        if readability_score < 60:
            suggestions.append({
                'category': 'Readability',
                'message': 'Break up long sentences to improve readability. Aim for 10-15 words per sentence.'
            })
        elif readability_score < 75:
            suggestions.append({
                'category': 'Readability',
                'message': 'Simplify some sentences for better comprehension and engagement.'
            })

        # Sentence length feedback
        if avg_sentence_length > 20:
            suggestions.append({
                'category': 'Readability',
                'message': f'Your average sentence length is {avg_sentence_length} words. Consider shorter sentences for better flow.'
            })

        return suggestions

    def _generate_length_suggestions(self, analysis: Dict) -> List[Dict[str, str]]:
        """Generate content length suggestions."""
        suggestions = []
        word_count = analysis.get('metrics', {}).get('word_count', 0)

        if word_count < 50:
            suggestions.append({
                'category': 'Length',
                'message': 'Your content is quite short. Aim for at least 50-100 words for better SEO and engagement.'
            })
        elif word_count > 500:
            suggestions.append({
                'category': 'Length',
                'message': f'Your content is {word_count} words. Consider breaking it into smaller chunks for social media.'
            })

        return suggestions

    def prioritize_suggestions(self, suggestions: List[Dict]) -> List[Dict]:
        """
        Prioritize suggestions by category importance.

        Args:
            suggestions (list): List of suggestions

        Returns:
            list: Prioritized suggestions
        """
        priority_order = {
            'Hook': 1,
            'Engagement': 2,
            'Readability': 3,
            'Length': 4,
            'Excellent': 5
        }

        return sorted(
            suggestions,
            key=lambda x: priority_order.get(x.get('category', 'Other'), 99)
        )
        