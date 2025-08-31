# src/services/seo_service.py

import re

class SeoService:
    """
    A simple service to analyze the SEO quality of a piece of text.
    """

    def __init__(self):
        # Keywords that are important for Windsor-Essex real estate SEO
        self.primary_keywords = [
            'windsor', 'essex', 'real estate', 'home', 'house', 'property',
            'listing', 'realtor', 'agent'
        ]
        self.location_keywords = [
            'tecumseh', 'lasalle', 'amherstburg', 'kingsville', 'leamington',
            'belle river', 'walkerville', 'south windsor'
        ]

    def analyze_content(self, text: str) -> dict:
        """
        Analyzes a piece of content and returns an SEO score and recommendations.
        """
        if not text:
            return {
                'score': 0,
                'recommendations': ['Content is empty.']
            }

        text_lower = text.lower()
        recommendations = []
        score = 0

        # 1. Keyword Presence (Max 50 points)
        primary_found = sum(1 for keyword in self.primary_keywords if keyword in text_lower)
        score += min(primary_found * 5, 50)
        if primary_found < 3:
            recommendations.append("Include more primary keywords like 'Windsor', 'real estate', 'home'.")

        # 2. Location Specificity (Max 20 points)
        location_found = sum(1 for keyword in self.location_keywords if keyword in text_lower)
        if location_found > 0:
            score += 20
        else:
            recommendations.append("Add a specific location (e.g., 'Tecumseh', 'South Windsor') to target local buyers.")

        # 3. Readability & Length (Max 20 points)
        word_count = len(text.split())
        if 50 <= word_count <= 150:
            score += 20
        elif 25 <= word_count < 50:
            score += 10
        else:
            recommendations.append(f"Content length is {word_count} words. Aim for 50-150 words for optimal engagement.")

        # 4. Call to Action (Max 10 points)
        cta_phrases = ['contact me', 'dm me', 'call now', 'learn more', 'schedule a viewing']
        if any(phrase in text_lower for phrase in cta_phrases):
            score += 10
        else:
            recommendations.append("Include a clear Call to Action (e.g., 'DM me for details').")

        return {
            'score': min(score, 100), # Ensure score doesn't exceed 100
            'recommendations': recommendations if recommendations else ["Looks good! This content is well-optimized."]
        }

# Create a single, global instance of the service that can be imported elsewhere
seo_service = SeoService()
