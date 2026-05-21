from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)


def semantic_score(
    user_answer,
    correct_answer
):

    answer = user_answer.strip().lower()

    # Empty answer

    if not answer:

        return 0

    # Very short answer

    if len(answer.split()) < 3:

        return 0

    # Random repeated letters

    if len(set(answer)) <= 3:

        return 0

    # Encode embeddings

    embeddings = model.encode([
        answer,
        correct_answer
    ])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    # Garbage / unrelated answers

    if similarity < 0.2:

        return 0

    elif similarity < 0.4:

        return 4

    elif similarity < 0.6:

        return 6

    elif similarity < 0.8:

        return 8

    return 10
