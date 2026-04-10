from openai import OpenAI
import os
from dotenv import load_dotenv
from config import MODEL

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_questions(topic: str):
    system_message = """
You are a helpful study buddy.
Ask 5 numbered questions about the topic.
Do not include answers or extra text.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": topic}
        ]
    )

    return response.choices[0].message.content


def grade_quiz(qa_string: str):
    system_message = """
You are a teacher grading answers.

Give:
- Score out of 5
- Feedback
- List weak questions like [1,3]

Be encouraging but honest.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": qa_string}
        ]
    )

    return response.choices[0].message.content