from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, index=True)
    is_revoked = Column(Boolean, default=False)