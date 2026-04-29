from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base


class DocumentAccess(Base):
    __tablename__ = "document_access"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    document_id = Column(Integer, nullable=False)
    query_id = Column(Integer, nullable=False)

    accessed_at = Column(DateTime, default=datetime.utcnow)