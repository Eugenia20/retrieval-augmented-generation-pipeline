from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime

from app.db.base import Base


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    query = Column(Text)
    response = Column(Text)
    language = Column(String)

    retrieved_docs = Column(Text)   # store as string

    timestamp = Column(DateTime, default=datetime.utcnow)