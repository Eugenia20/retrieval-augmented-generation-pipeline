import json

from app.models.query import Query
from app.models.evaluation import Evaluation
from app.models.document import Document
from app.models.document_access import DocumentAccess

from app.rag.pipeline.pipeline import process_query
from app.core.logger import logger


async def handle_query(db, user_id: int, employee_id: str, user_department: str, query: str):
    try:
        # =========================
        # RUN PIPELINE (ASYNC)
        # =========================
        result = await process_query(query, user_department)

        answer = result["answer"]
        language = result.get("language", "en")
        sources = result.get("sources", [])

        # =========================
        # SAVE QUERY
        # =========================
        db_query = Query(
            user_id=user_id,
            employee_id=employee_id,
            question=query,
            answer=answer,
            language=language,
            retrieved_docs=json.dumps(sources)
        )

        db.add(db_query)
        db.flush()  # get ID

        # =========================
        # SAVE EVALUATION
        # =========================
        eval_data = result.get("evaluation")

        if eval_data:
            db_eval = Evaluation(
                query_id=db_query.id,
                relevance_score=eval_data.get("relevance_score"),
                hallucination_flag=eval_data.get("hallucination_flag"),
                confidence_score=eval_data.get("confidence_score")
            )
            db.add(db_eval)

        # =========================
        # LOG DOCUMENT ACCESS
        # =========================
        doc_ids = list(set([
            d["document_id"] for d in sources
        ]))

        for doc_id in doc_ids:
            access_log = DocumentAccess(
                user_id=user_id,
                document_id=doc_id,
                query_id=db_query.id
            )
            db.add(access_log)

        # =========================
        # COMMIT EVERYTHING ONCE
        # =========================
        db.commit()

        # =========================
        # MAP DOCUMENT IDS → FILENAMES
        # =========================
        docs_from_db = db.query(Document).filter(
            Document.id.in_(doc_ids)
        ).all()

        doc_map = {doc.id: doc.filename for doc in docs_from_db}

        clean_sources = [
            {
                "document_id": d["document_id"],
                "filename": doc_map.get(d["document_id"], "unknown")
            }
            for d in sources
        ]

        # =========================
        # LOG SUCCESS
        # =========================
        logger.info(f"RAG query processed: user={user_id}, query='{query}'")

        return {
            "answer": answer,
            "confidence": result.get("confidence"),
            "sources": clean_sources,
            "evaluation": eval_data
        }

    except Exception as e:
        db.rollback()

        logger.error(f"RAG ERROR: {str(e)}")

        return {
            "answer": "Something went wrong while processing your request.",
            "error": str(e)
        }