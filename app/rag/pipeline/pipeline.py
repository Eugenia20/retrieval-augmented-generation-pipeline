from app.rag.language.detector import detect_language
from app.rag.language.translator import translate_to_english, translate_from_english
from app.rag.components.retriever import retrieve_documents
from app.rag.components.generator import generate_answer
from app.services.evaluation_service import evaluate_response


SUPPORTED_LANGUAGES = ["en", "ru", "zh"]


def process_query(query: str, user_department: str):
    # =========================
    # 1. Detect language
    # =========================
    from app.rag.language.language_controller import detect_target_language

    detected_language = detect_language(query)

    if detected_language not in SUPPORTED_LANGUAGES:
        detected_language = "en"

    target_language = detect_target_language(query, detected_language)

    # =========================
    # 2. Translate only if needed
    # =========================
    translated_query = (
        translate_to_english(query)
        if detected_language != "en"
        else query
    )

    # =========================
    # 3. Retrieve documents
    # =========================
    docs = retrieve_documents(
        translated_query,
        "en",
        user_department,
        k=5
    )

    texts = [d["text"] for d in docs]

    context = "\n\n---\n\n".join(texts)

    # =========================
    # 4. Build context
    # =========================
    context = "\n\n---\n\n".join(docs)

    # =========================
    # 5. Generate answer
    # =========================
    answer_en = generate_answer(translated_query, context, target_language)

    # =========================
    # 6. Translate back ONLY if needed
    # =========================
    if target_language != "en":
        final_answer = translate_from_english(answer_en, target_language)
    else:
        final_answer = answer_en

    # =========================
    # 7. Confidence
    # =========================
    confidence = min(1.0, len(docs) / 5)

    # =========================
    # 8. Evaluation
    # =========================
    evaluation = evaluate_response(
        query=translated_query,
        response=answer_en,
        docs=docs
    )

    # =========================
    # 9. Return structured output
    # =========================
    return {
        "query": query,
        "translated_query": translated_query,
        "detected_language": detected_language,
        "target_language": target_language,
        "answer": final_answer,
        "confidence": confidence,
        "sources": docs,
        "evaluation": evaluation
    }