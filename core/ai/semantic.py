from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def semantic_score(user_answer, correct_answer):

    answer = user_answer.strip().lower()

    if not answer:
        return 0

    if len(answer.split()) < 3:
        return 0

    if len(set(answer)) <= 3:
        return 0

    texts = [
        answer,
        correct_answer.lower()
    ]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    if similarity < 0.2:
        return 0

    elif similarity < 0.4:
        return 4

    elif similarity < 0.6:
        return 6

    elif similarity < 0.8:
        return 8

    return 10