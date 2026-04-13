import logo from '../logo.svg';
import './App.css';
import Input from "./Input"
import Button from './Button';
import { useState } from 'react'

function App() {

  const [topic, setTopic] = useState("")
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState([])
  const [feedback, setFeedback] = useState("")
  const [weakQuestions, setWeakQuestions] = useState([])

  const handleGenerateQuiz = async () => {
    const response = await fetch("http://127.0.0.1:8000/quiz", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ topic: topic })
    })

    const data = await response.json()
    setQuestions(data.questions)
    setAnswers(new Array(data.questions.length).fill(""))
  }

  const handleAnswerChange = (value, index) => {
    const newAnswers = [...answers]
    newAnswers[index] = value
    setAnswers(newAnswers)
  }

  const handleSubmit = async ()=>{
    console.log({
        topic: topic,
        questions: questions,
        answers: answers
      })
    const response = await fetch("http://127.0.0.1:8000/submit",{
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        topic: topic,
        questions: questions,
        answers: answers
      })
    })

    const data = await response.json()
    setFeedback(data.feedback)
    setWeakQuestions(data.weak_questions)

  }

  return (
    <div className="container">
      <input className="topic-input" placeholder='Enter Topic' onChange={(e) => setTopic(e.target.value)} name="topic" value={topic} />
      <button className="btn" onClick={handleGenerateQuiz} disabled={!topic}>Generate Quiz</button>
      {questions.map((q, index) => (
        <div className={`question-card ${
      weakQuestions.includes(index + 1) ? "weak" : ""
    }`} key={index}
        style = {{
          color: weakQuestions.includes(index+1) ? "#ff0000" : "black"
        }}
        >
          <p className="question-text">Q{index + 1}: {q}</p>
          <input className="answer-input"
            value={answers[index] || ""}
            onChange={(e) => handleAnswerChange(e.target.value, index)}
            placeholder='Enter Answer...'
          />

        </div>

      ))}
      <button className="btn submit" onClick={handleSubmit}>Submit Answers</button>
      {feedback && (
        <div className="feedback-box">
          <p><strong>Feedback: {feedback}</strong></p>
          {weakQuestions.length > 0 && (
            <p className="weak-text">Review these questions: {weakQuestions.join(", ")}</p>
          )}
          
          {/* {weakQuestions.map((q, index)=>{
            <p key="{index}">Q: {q}</p>
          })} */}
        </div>

      )}
    </div>
  )
}

export default App;
