# src/services/learning_algorithm_service.py

import random
from src.models.social_media import db, TrainingData
# Import our new SeoService!
from src.services.seo_service import seo_service

class LearningAlgorithmService:
    """
    Service for learning from user-provided training data and generating
    new, SEO-optimized content recommendations.
    """

    def generate_content_recommendations(self, topic: str, content_type: str) -> dict:
        """
        Generates content recommendations based on a topic and learned brand voice.
        """
        # Fetch relevant training data from the database
        training_examples = TrainingData.query.filter_by(post_type=content_type).limit(10).all()

        if not training_examples:
            return {
                "success": False,
                "error": f"Not enough training data for content type '{content_type}'. Please add more examples."
            }

        recommendations = []
        # Generate 3 recommendations
        for i in range(3):
            # Pick a random training example to use as a base
            base_example = random.choice(training_examples)
            
            # Create a new piece of content (this is a simplified generation logic)
            focus = f"Variation {i+1} based on your '{base_example.post_type}' style"
            
            # A simple generation rule: combine the user's topic with the style of a past post.
            # A more advanced AI would use a language model here.
            new_content = f"{topic}.\n\n(Inspired by your post: '{base_example.content[:50]}...')"

            # --- THIS IS THE NEW PART ---
            # Analyze the generated content using our new SEO service
            seo_analysis = seo_service.analyze_content(new_content)
            
            recommendations.append({
                "content": new_content,
                "focus": focus,
                "hashtags": ["#WindsorRealEstate", f"#{content_type}"], # Placeholder hashtags
                "seo_score": seo_analysis.get('score'),
                "seo_recommendations": seo_analysis.get('recommendations')
            })

        return {
            "success": True,
            "recommendations": recommendations
        }

# Create a single, global instance of the service
learning_algorithm_service = LearningAlgorithmService()
