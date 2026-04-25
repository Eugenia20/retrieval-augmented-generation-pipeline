import json
from app.models.query import Query
from app.models.evaluation import Evaluation
from app.rag.pipeline.pipeline import process_query


def handle_query(db, user_id: int, query: str):
    result = process_query(query)

    # =========================
    # Save query
    # =========================
    db_query = Query(
        user_id=user_id,
        query=query,
        response=result["answer"],
        language=result["language"],
        retrieved_docs=json.dumps(result["sources"])
    )

    db.add(db_query)
    db.commit()
    db.refresh(db_query)

    # =========================
    # Save evaluation
    # =========================
    eval_data = result["evaluation"]

    db_eval = Evaluation(
        query_id=db_query.id,
        relevance_score=eval_data["relevance_score"],
        hallucination_flag=eval_data["hallucination_flag"],
        confidence_score=eval_data["confidence_score"]
    )

    db.add(db_eval)
    db.commit()

    return result