
def parse_questions(text: str):
    lines = text.split("\n")
    questions = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(".", 1)
        if len(parts) > 1:
            questions.append(parts[1].strip())

    return questions


def extract_weak_questions(feedback: str):
    weak = []

    if "[" not in feedback or "]" not in feedback:
        return weak

    start = feedback.index("[")
    end = feedback.index("]")

    numbers = feedback[start + 1:end].split(",")

    for n in numbers:
        n = n.strip()
        if n.isdigit():
            weak.append(int(n))

    return weak