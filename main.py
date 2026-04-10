from dotenv import load_dotenv
from openai import OpenAI
import os
import datetime
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
FILE_PATH = "quiz_history.json"


def load_history():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except:
                return []
    return []


def save_history(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


def parse_questions(question_text):
    lines = question_text.split("\n")
    cleaned = []

    for line in lines:
        if line.strip():
            parts = line.split(".", 1)
            if len(parts) > 1:
                cleaned.append(parts[1].strip())

    return cleaned


def extract_weak_questions(feedback):
    weak = []

    if "[" in feedback and "]" in feedback:
        start = feedback.index("[")
        end = feedback.index("]")

        numbers_str = feedback[start + 1:end]
        parts = numbers_str.split(",")

        for p in parts:
            p = p.strip()
            if p:
                weak.append(int(p))

    return weak



while True:
    choice = input(
        "\nPlease Choose:\n1. New Quiz\n2. View History\n3. Quit\n> "
    )


    if choice == "1":
        user_input = input("\nWhat would you like to study? ")

        system_message = """
You are a helpful study buddy.
Ask 5 questions about the user's topic.

Rules:
- Return only numbered questions
- No answers
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ]
        )

        question_text = response.choices[0].message.content
        cleaned_questions = parse_questions(question_text)

        user_answers = []

        for i, q in enumerate(cleaned_questions):
            print(f"\nQ{i+1}: {q}")
            user_answers.append(input("> "))

        qa_string = ""
        for i in range(len(cleaned_questions)):
            qa_string += f"Q{i+1}: {cleaned_questions[i]}\nA{i+1}: {user_answers[i]}\n-----\n\n"

        feedback_system_msg = """
You are a teacher grading a quiz.

Return:
Score (out of 5)
Feedback
Weak questions in format: [1, 3]

Be clear and encouraging.
"""

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": feedback_system_msg},
                {"role": "user", "content": qa_string}
            ]
        )

        feedback = res.choices[0].message.content

        weak_questions = extract_weak_questions(feedback)

  
        for q_num in weak_questions:
            print(f"\nRetry Q{q_num}: {cleaned_questions[q_num - 1]}")
            new_answer = input("> ")
            user_answers[q_num - 1] = new_answer

        quiz_data = {
            "topic": user_input,
            "questions": cleaned_questions,
            "answers": user_answers,
            "feedback": feedback,
            "score": None,
            "date": str(datetime.datetime.now())
        }

        print("\n===== QUIZ RESULTS =====")
        print(qa_string)
        print("\n===== FEEDBACK =====")
        print(feedback)

        history = load_history()
        history.append(quiz_data)
        save_history(history)

    elif choice == "2":
        data = load_history()

        if not data:
            print("\nNo History Available Yet.")
        else:
            for i, quiz in enumerate(data):
                print(f"\n===== QUIZ {i+1} =====")
                print(f"Topic: {quiz['topic']}\n")

                for j in range(len(quiz["questions"])):
                    print(f"Q{j+1}: {quiz['questions'][j]}")
                    print(f"A{j+1}: {quiz['answers'][j]}\n")

                print(f"Feedback: {quiz['feedback']}")
                print(f"Score: {quiz['score']}")
                print(f"Date: {quiz['date']}")
                print("====================")

    elif choice == "3":
        print("Goodbye 👋")
        break

    else:
        print("Invalid Choice")