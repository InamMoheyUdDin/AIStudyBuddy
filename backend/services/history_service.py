import json
import os
from config import FILE_PATH


def load_history():
    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_history(data):
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def view_history():
    data = load_history()

    if not data:
        print("No history found.")
        return

    for i, quiz in enumerate(data):
        print(f"\n===== QUIZ {i+1} =====")
        print("Topic:", quiz["topic"])

        for j, q in enumerate(quiz["questions"]):
            print(f"Q{j+1}: {q}")
            print(f"A{j+1}: {quiz['answers'][j]}")

        print("Feedback:", quiz["feedback"])
        print("Score:", quiz.get("score"))
        print("Date:", quiz.get("date"))