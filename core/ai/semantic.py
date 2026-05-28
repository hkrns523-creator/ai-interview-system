from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

def semantic_score(user_answer, correct_answer):

    answer = user_answer.strip().lower()

    # Basic validations
    if not answer:
        return 0

    if len(answer.split()) < 3:
        return 0

    if len(set(answer)) <= 3:
        return 0

    # Generate embeddings
    embeddings = model.encode([
        answer,
        correct_answer.lower()
    ])

    # Calculate semantic similarity
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    # Score mapping
    if similarity < 0.30:
        return 0

    elif similarity < 0.50:
        return 4

    elif similarity < 0.70:
        return 6

    elif similarity < 0.85:
        return 8

    return 10