def generate_feedback(semantic, keyword, grammar):

    feedback = []

    if semantic >= 8:
        feedback.append("Good technical understanding.")

    else:
        feedback.append("Answer lacks technical depth.")

    if keyword >= 8:
        feedback.append("Important concepts covered.")

    else:
        feedback.append("Missing important keywords.")

    if grammar >= 8:
        feedback.append("Communication is clear.")

    else:
        feedback.append("Improve sentence clarity.")

    return feedback