from fastapi import FastAPI
from pydantic import BaseModel, Field
from services.ai_service import generate_questions, grade_quiz
from utils.parser import parse_questions, extract_weak_questions
from services.history_service import load_history, save_history
from typing import List
import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizRequest(BaseModel):
    topic: str = Field(...)

class SubmitRequest(BaseModel):
    topic: str = Field(...)
    qestions: List[str] = Field(...)
    answers: List[str] = Field(...)


@app.get("/")
def home():
    return {"message": "API is working"}

@app.get("/history")
def get_history():
    history = load_history()

    return{"history": history}

@app.post("/quiz")
def gen_questions(request: QuizRequest):
    raw_questions = generate_questions(request.topic)
    parsed_questions = parse_questions(raw_questions)
    return{
        "questions": parsed_questions
    }

@app.post("/submit")
def submit_request(request: SubmitRequest):
    qa_string = ""

    if len(request.questions) != len(request.answers):
        return {"error": "Questions and answers count must match"}

    for i in range(len(request.qestions)):
        qa_string += f"Q{i+1}: {request.questions[i]}\n"
        qa_string += f"A{i+1}: {request.answers[i]}\n\n"

    feedback = grade_quiz(qa_string)
    weak_questions = extract_weak_questions(feedback)

    history = load_history()
    history.append(
        {
            "topic": request.topic,
            "questions": request.qestions,
            "answers": request.answers,
            "feedback": feedback,
            "score": None,
            "date": str(datetime.datetime.now())

        }
    )
    save_history(history)

    return {
        "feedback": feedback,
        "weak_questions": weak_questions
    }
