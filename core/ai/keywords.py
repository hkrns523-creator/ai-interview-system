def keyword_score(answer, keywords):

    answer = answer.lower().strip()

    # Garbage detection

    if len(answer.split()) < 3:

        return 0

    if len(set(answer)) <= 3:

        return 0

    found = 0

    for word in keywords:

        if word.lower() in answer:

            found += 1

    if len(keywords) == 0:

        return 0

    score = (

        found / len(keywords)

    ) * 10

    return round(score, 2)