from dotenv import load_dotenv
from openai import OpenAI
import os
import datetime
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

while True:
    choice = input("Please Choose:\n1. New Quiz\n2. View History\n3.Quit\n\n")

    if choice == "1":
        user_input = input("What is something you would like to study: ")

        system_message = """ You are a helpful study buddy asking 5 questions about a topic the user chooses.
        Return the questions in a numbered list format.
        Do not provide any answers or any extra text

        If the user ask a question that is inappropriate or explicit replay: "Sorry that is inappropriate. Would you like to ask another question."
        """

        # response = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages = [
        #         {"role": "system", "content": system_message},
        #         {"role": "user", "content": user_input}
        #     ]
        # )

        # question = response.choices[0].message.content

        question = """1. What are the different types of loops available in Python, and how do they differ from each other?
        2. How does a `for` loop work in Python, and when would you use it?
        3. Can you explain the purpose of a `while` loop and provide an example to illustrate its usage?
        4. What is the `break` statement in loops, and how can it be used to control loop execution?
        5. How can you use the `continue` statement in a loop, and what effect does it have on loop iterations?"""

        lines = question.split("\n")
        cleaned_questions = []

        for line in lines:
            if line.strip():
                parts = line.split(".", 1)
                if len(parts)>1:
                    cleaned = parts[1].strip()
                    cleaned_questions.append(cleaned)

        user_answers = []

        for i, q in enumerate(cleaned_questions):
            print(f"Q{i+1}: {q}")
            answer = input("> ")
            user_answers.append(answer)

        qa_string = ""

        for i in range(len(cleaned_questions)):
            qa_string += f"Q{i+1}: {cleaned_questions[i]}\nA{i+1}: {user_answers[i]}\n-----\n\n"


        feedback_system_msg = """You are a teacher providing feedback to the answers provided by a student.
        Give a grade out of 5.
        Provide feedback to the student.

        Score:
        Feedback:

        Be encouraging but honest.
        """

        # res = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages = [
        #         {"role": "system", "content": feedback_system_msg},
        #         {"role": "user", "content": qa_string}
        #     ]
        # )

        # feedback = res.choices[0].message.content

        feedback = "great"

        quiz_data = {
            "topic": user_input,
            "questions": cleaned_questions,
            "answers": user_answers,
            "feedback": feedback,
            "score": None,
            "date": str(datetime.datetime.now())
        }

        print("===== QUIZ RESULTS =====")
        print(qa_string)
        print("===== FEEDBACK =====")
        print(feedback)

        file_path = "quiz_history.json"

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                except:
                    data = []
        else:
            data = []

        data.append(quiz_data)

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    elif choice == "2":
        file_path = "quiz_history.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                except:
                    data = []
        else:
            data = []
        
        if not data:
            print("No History Available Yet.")
        else:
            for i, quiz in enumerate(data):
                print(f"===== QUIZ {i+1} =====\n")
                print(quiz["topic"])

                for j in range(len(quiz["questions"])):
                    print(f'Q{j+1}: {quiz["questions"][j]}')
                    print(f'A{j+1}: {quiz["answers"][j]}\n')
                
                print(f'Feedback: {quiz["feedback"]}')
                print(f'Score: {quiz["score"]}')
                print(quiz["date"])
                print("============\n")
    elif choice == "3":
        break
    else:
        print("Invalid Choice")
        
