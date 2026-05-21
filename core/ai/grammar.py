import re


def grammar_score(answer):

    answer = answer.strip()

    # Empty answer
    if not answer:
        return 0

    words = answer.split()

    # Very short answers
    if len(words) < 3:
        return 0

    # Remove special characters
    clean_text = re.sub(
        r'[^a-zA-Z ]',
        '',
        answer
    )

    total_chars = len(
        clean_text.replace(" ", "")
    )

    # No valid text
    if total_chars == 0:
        return 0

    # Vowel analysis
    vowels = "aeiou"

    vowel_count = sum(

        1 for char in clean_text.lower()

        if char in vowels

    )

    vowel_ratio = vowel_count / total_chars

    # Gibberish detection
    # Example:
    # "fefjwe" -> low quality
    # "asdfgh" -> gibberish
    if vowel_ratio < 0.25:
        return 0

    # Base score
    score = 10

    # Repeated words check
    unique_ratio = len(set(words)) / len(words)

    if unique_ratio < 0.5:
        score -= 2

    # Missing punctuation
    if not re.search(r'[.!?]$', answer):
        score -= 1

    # Starts lowercase
    if answer[0].islower():
        score -= 1

    # Too short sentence
    if len(words) < 8:
        score -= 2

    # Too many repeated characters
    repeated_chars = re.findall(
        r'(.)\1{3,}',
        answer.lower()
    )

    if repeated_chars:
        score -= 3

    return max(round(score, 1), 0)