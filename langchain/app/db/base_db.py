"""
    BASE FILE FOR DB
"""

# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.user_models import User
from app.models.conversational_models import Message, Conversation
from app.db.base_class import Base  # noqa
