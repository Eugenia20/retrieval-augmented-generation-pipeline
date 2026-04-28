from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    department = Column(String, nullable=True)
    uploaded_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)