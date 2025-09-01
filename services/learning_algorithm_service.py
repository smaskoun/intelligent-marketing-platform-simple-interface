# services/learning_algorithm_service.py

import random
from models.social_media import db, TrainingData
from services.seo_service import seo_service

class LearningAlgorithmService:
    """
    Service for learning from user-provided training data and generating
    new, SEO-optimized content recommendations.
    """

    def generate_content_recommendations(self, user_id: str, content_type: str, platform: str) -> dict:
        """
        Generates content recommendations based on a topic and learned brand voice.
        """
        # Fetch relevant training data from the database for the specific user
        training_examples = TrainingData.query.filter_by(user_id=user_id, post_type=content_type).limit(10).all()

        # --- THIS IS THE FIX ---
        # If there is no training data for this specific content type,
        # return a helpful error message that the frontend can display.
        if not training_examples:
            return {
                "success": False,
                "error": f"No training data found for '{content_type}'. Please add examples in the 'Train Brand Voice' tab first."
            }
        # ----------------------

        recommendations = []
        # Generate 3 recommendations
        for i in range(3):
            base_example = random.choice(training_examples)
            focus = f"Variation {i+1} based on your '{base_example.post_type}' style"
            topic = f"A new post about {content_type.replace('_', ' ')}"
            new_content = f"{topic}.\n\n(Inspired by your post: '{base_example.content[:50]}...')"
            seo_analysis = seo_service.analyze_content(new_content)
            
            recommendations.append({
                "content": new_content,
                "focus": focus,
                "hashtags": ["#WindsorRealEstate", f"#{content_type}"],
                "seo_score": seo_analysis.get('score'),
                "seo_recommendations": seo_analysis.get('recommendations')
            })

        # If everything is successful, return the recommendations.
        return {
            "success": True,
            "recommendations": recommendations
        }

# Create a single, global instance of the service
learning_algorithm_service = LearningAlgorithmService()
