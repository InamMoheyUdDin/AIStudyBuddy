import datetime
from services.ai_service import generate_questions, grade_quiz
from services.history_service import load_history, save_history
from utils.parser import parse_questions, extract_weak_questions


def run_quiz():
    topic = input("What do you want to study? ")

    raw_questions = generate_questions(topic)
    questions = parse_questions(raw_questions)

    answers = []

    for i, q in enumerate(questions):
        print(f"Q{i+1}: {q}")
        answers.append(input("> "))

    qa_string = ""
    for i in range(len(questions)):
        qa_string += f"Q{i+1}: {questions[i]}\nA{i+1}: {answers[i]}\n\n"

    feedback = grade_quiz(qa_string)

    weak = extract_weak_questions(feedback)

    # retry weak questions
    for q_num in weak:
        if 1 <= q_num <= len(questions):
            print(f"\nRetry Q{q_num}: {questions[q_num - 1]}")
            answers[q_num - 1] = input("> ")

    quiz_data = {
        "topic": topic,
        "questions": questions,
        "answers": answers,
        "feedback": feedback,
        "score": None,
        "date": str(datetime.datetime.now())
    }

    history = load_history()
    history.append(quiz_data)
    save_history(history)

    print("\n===== RESULTS =====")
    print(qa_string)
    print("\n===== FEEDBACK =====")
    print(feedback)