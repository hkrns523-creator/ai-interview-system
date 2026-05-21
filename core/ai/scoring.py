from .semantic import semantic_score
from .keywords import keyword_score
from .grammar import grammar_score
from .feedback import generate_feedback


def evaluate_answer(
    user_answer,
    correct_answer,
    keywords
):

    semantic = semantic_score(
        user_answer,
        correct_answer
    )

    keyword = keyword_score(
        user_answer,
        keywords
    )

    grammar = grammar_score(
        user_answer
    )

    final_score = (

    semantic * 0.6 +

    keyword * 0.3 +

    grammar * 0.1
    )

    feedback = generate_feedback(
        semantic,
        keyword,
        grammar
    )

    return {

    "semantic":
    round(float(semantic), 2),

    "keyword":
    round(float(keyword), 2),

    "grammar":
    round(float(grammar), 2),

    "final_score":
    round(float(final_score), 2),

    "feedback":
    feedback
}