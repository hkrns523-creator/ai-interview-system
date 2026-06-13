import re
import nltk
from textblob import TextBlob

for resource in [
    'tokenizers/punkt',
    'tokenizers/punkt_tab',
    'taggers/averaged_perceptron_tagger',
    'taggers/averaged_perceptron_tagger_eng',
]:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource.split('/')[-1], quiet=True)


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

    # Vowel analysis (quick gibberish filter)
    vowels = "aeiou"

    vowel_count = sum(
        1 for char in clean_text.lower()
        if char in vowels
    )

    vowel_ratio = vowel_count / total_chars

    # Gibberish detection
    if vowel_ratio < 0.25:
        return 0

    # Base score
    score = 10

    blob = TextBlob(answer)
    corrected = blob.correct()

    original_words = answer.lower().split()
    corrected_words = str(corrected).lower().split()

    if len(original_words) == len(corrected_words):
        misspelled = sum(
            1 for o, c in zip(original_words, corrected_words)
            if o != c
        )
        misspell_ratio = misspelled / len(original_words)

        if misspell_ratio > 0.3:
            score -= 3
        elif misspell_ratio > 0.15:
            score -= 1.5

    tokens = nltk.word_tokenize(answer)
    pos_tags = nltk.pos_tag(tokens)

    has_noun = any(tag.startswith('NN') for _, tag in pos_tags)
    has_verb = any(tag.startswith('VB') for _, tag in pos_tags)

    # Missing core sentence structure (no subject/predicate-like pattern)
    if not (has_noun and has_verb):
        score -= 2

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