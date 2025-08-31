from ..models.social_media import db, TrainingData
import random

class LearningAlgorithmService:
    """
    Service for generating content recommendations based on user-provided training data.
    """
    
    def generate_content_recommendations(self, user_id, content_type, platform):
        """
        Generates new content by using the user's training data as a foundation.
        """
        # 1. Fetch relevant training data from the database for the specified user and content type.
        training_posts = db.session.query(TrainingData).filter_by(
            user_id=user_id, 
            post_type=content_type
        ).all()

        # 2. If no specific training data is found, get some general posts from the user.
        if not training_posts:
            training_posts = db.session.query(TrainingData).filter_by(user_id=user_id).limit(10).all()

        # 3. If there is still no data at all, return a helpful message.
        if not training_posts:
            return [{
                "template_id": "no_data_01",
                "generated_content": "I need more examples to learn your style! Please use the 'Train Brand Voice' feature to add at least 5-10 of your past posts.",
                "reason": "No training data found in the AI Memory."
            }]

        # 4. This is where the "AI" logic happens. For now, we will use a simple but effective strategy:
        #    - Pick a random training post.
        #    - Create a few new variations based on its content.
        
        chosen_post = random.choice(training_posts)
        base_content = chosen_post.content

        # Simple templates for generating variations
        recommendations = [
            {
                "template_id": "variation_A",
                "generated_content": f"Here's a new take on a successful post: \"{base_content}\" - What if we focused more on the call to action?",
                "reason": f"Based on your successful '{chosen_post.post_type}' post."
            },
            {
                "template_id": "variation_B",
                "generated_content": f"Inspired by your style: \"{base_content}\" - Let's try making the opening hook more emotional.",
                "reason": f"Learned from post ID {chosen_post.id}."
            },
            {
                "template_id": "variation_C",
                "generated_content": f"Let's try this angle: \"{base_content}\" - We could also add some relevant market stats to this.",
                "reason": "Adapting your proven content style."
            }
        ]
        
        return recommendations

# Create a single, global instance of the service that our routes can use.
learning_algorithm_service = LearningAlgorithmService()
