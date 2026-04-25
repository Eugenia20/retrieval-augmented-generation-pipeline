from sqlalchemy import Column, Integer, Float, ForeignKey

from app.db.base import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"))

    relevance_score = Column(Float)
    hallucination_flag = Column(Integer)
    confidence_score = Column(Float)