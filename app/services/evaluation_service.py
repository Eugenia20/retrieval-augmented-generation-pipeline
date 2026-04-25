def evaluate_response(query: str, answer: str):


    relevance_score = 0.8
    confidence_score = 0.75

    hallucination_flag = False

    if "unknown" in answer.lower():
        hallucination_flag = True

    return {
        "relevance_score": relevance_score,
        "confidence_score": confidence_score,
        "hallucination_flag": hallucination_flag
    }