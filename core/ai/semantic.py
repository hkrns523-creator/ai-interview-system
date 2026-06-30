from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def semantic_score(user_answer, correct_answer):

    answer = user_answer.strip().lower()

    if not answer:
        return 0

    if len(answer.split()) < 3:
        return 0

    if len(set(answer)) <= 3:
        return 0

    model = get_model()

    embeddings = model.encode([
        answer,
        correct_answer.lower()
    ])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    if similarity < 0.30:
        return 0

    elif similarity < 0.50:
        return 4

    elif similarity < 0.70:
        return 6

    elif similarity < 0.85:
        return 8

    return 10