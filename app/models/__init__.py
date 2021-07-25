from app.core import db
from .base import BaseModel


@db.register(collection="users")
class User(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
