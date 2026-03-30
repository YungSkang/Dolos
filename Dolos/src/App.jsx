import { useState } from 'react'
import heroImg from './assets/hero.png'
import './App.css'


function App() {

  const [password, setPassword] = useState('')
  const [result, setResult] = useState(null)

  const handleClick = async (e) => {
    e.preventDefault()
    try {
      const response = await fetch('http://127.0.0.1:8000/analyze-password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ password: password })
      })

      const data = await response.json()
      setResult(data) // store result

    } catch (error) {
      console.error("Error:", error)
    }
  
  }

return (
    <section id="center">
      
      <div className="hero">
        <img src={heroImg} alt="" />
      </div>

      <h1>Password Strength Checker</h1>

      <form>
        <input
          type="text"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleClick}>
          Check Strength
        </button>
      </form>

      {/* 🟢 RESULT DISPLAY */}
      {result && (
        <div>
          <h3>Result:</h3>
          <p><strong>Score:</strong> {result.score}</p>
          <p><strong>Strength:</strong> {result.strength}</p>
        </div>
      )}

    </section>
  )
}


export default App
