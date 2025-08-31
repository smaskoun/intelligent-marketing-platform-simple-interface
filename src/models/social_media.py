from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the database extension. 
# It's better to do this in a central place, like a models/__init__.py, 
# but for now, we will keep it simple.
db = SQLAlchemy()

# This class defines the structure for the 'training_data' table in your database.
class TrainingData(db.Model):
    """
    Represents a single piece of content provided by the user to train the AI.
    This is the ONLY table our new, simplified application needs from this file.
    """
    __tablename__ = 'training_data'

    # Defines the 'id' column: an integer that is the primary key for the table.
    id = db.Column(db.Integer, primary_key=True)
    
    # Defines the 'user_id' column: a string to identify the user.
    user_id = db.Column(db.String(80), nullable=False, index=True)
    
    # Defines the 'content' column: a long text field for the post's content.
    content = db.Column(db.Text, nullable=False)
    
    # Defines the 'image_url' column: a string for the image link, which can be empty.
    image_url = db.Column(db.String(2048), nullable=True)
    
    # Defines the 'post_type' column: a string for the category (e.g., 'listing', 'sold').
    post_type = db.Column(db.String(50), nullable=False)
    
    # Defines the 'created_at' column: a timestamp that defaults to the current time.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TrainingData {self.id} for user {self.user_id}>'

    def to_dict(self):
        """Returns a dictionary representation of the model."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "image_url": self.image_url,
            "post_type": self.post_type,
            "created_at": self.created_at.isoformat()
        }

