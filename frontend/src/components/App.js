import logo from '../logo.svg';
import './App.css';
import Input from "./Input"
import Button from './Button';
import { useState } from 'react'

function App() {

  const [topic, setTopic] = useState("")
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState([])

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

  const handleAnswerChange = (value, index)=>{
    const newAnswers = [...answers]
    newAnswers[index] = value
    setAnswers(newAnswers)
  }

  return (
    <div>
      <input placeholder='Enter Topic' onChange={(e) => setTopic(e.target.value)} name="topic" value={topic} />
      <button onClick={handleGenerateQuiz} disabled={!topic}>Generate Quiz</button>
      {questions.map((q, index) => (
        <div key={index}>
          <p>Q{index + 1}: {q}</p>
          <input 
          value={answers[index] || ""}
          onChange={(e)=> handleAnswerChange(e.target.value, index)}
          placeholder='Enter Answer...'
          />

        </div>
        
      ))}
    </div>
  )
}

export default App;
