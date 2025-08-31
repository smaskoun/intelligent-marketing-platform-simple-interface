from ..models import db
from ..models.social_media import TrainingData

class BrandVoiceService:
    def add_training_data(self, user_id, content, image_url, post_type):
        """
        Creates a new training data entry and saves it to the database.
        This method is called by the route in brand_voice.py.
        """
        try:
            # Create an instance of our SQLAlchemy database model
            # This represents a new row in our 'training_data' table.
            new_training_entry = TrainingData(
                user_id=user_id,
                content=content,
                image_url=image_url,
                post_type=post_type
            )

            # Add the new entry to the current database session
            db.session.add(new_training_entry)

            # Commit the session to permanently save the new row in the database
            db.session.commit()

            # Return a simple dictionary with the new entry's details.
            # This can be useful for the frontend or for logging.
            return {
                "id": new_training_entry.id,
                "content": new_training_entry.content,
                "post_type": new_training_entry.post_type,
                "created_at": new_training_entry.created_at.isoformat()
            }
        except Exception as e:
            # If any error occurs during the database operation...
            # Roll back the changes to ensure the database remains in a consistent state.
            db.session.rollback()
            
            # Print the error to the console for debugging purposes.
            print(f"Database error in BrandVoiceService: {e}")
            
            # Re-raise the exception so the route that called this method
            # knows something went wrong and can return a 500 error.
            raise e

