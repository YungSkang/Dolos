import { useState } from 'react'
import heroImg from './assets/hero.png'
import EyeField from './EyeField'
import './App.css'


const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

// mapping of strength tiers to bar percentages and colors

const STRENGTH_PERCENT = {
  "Compromised": 5,
  "Very Weak":   15,
  "Weak":        35,
  "Fair":        60,
  "Strong":      85,
  "Very Strong": 100,
}

const STRENGTH_COLOR = {
  "Compromised": "#ff0000",
  "Very Weak":   "#ff4500",
  "Weak":        "#ff8c00",
  "Fair":        "#ffd700",
  "Strong":      "#7cfc00",
  "Very Strong": "#00ff9f",
}

const STRENGTH_CLASS = {
  "Compromised": "compromised",
  "Very Weak":   "very-weak",
  "Weak":        "weak",
  "Fair":        "fair",
  "Strong":      "strong",
  "Very Strong": "very-strong",
}

// generate a strong random password locally using the Web Crypto API

function generateStrongPassword(length = 14) {
  const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-='
  const array = new Uint8Array(length)
  crypto.getRandomValues(array)
  return Array.from(array).map(b => charset[b % charset.length]).join('')
}

// main app component

export default function App() {
  const [password, setPassword]         = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [result, setResult]             = useState(null)
  const [loading, setLoading]           = useState(false)
  const [copied, setCopied]             = useState(false)
  const [generatedPwd, setGeneratedPwd] = useState(() => generateStrongPassword())

  const [showPersonalForm, setShowPersonalForm] = useState(false)
  const [personalInfo, setPersonalInfo]         = useState({
    first_name: '', last_name: '', birthdate: '', pet_name: '', city_name: ''
  })
  const [personalResults, setPersonalResults]   = useState([])
  const [personalLoading, setPersonalLoading]   = useState(false)

  // handle password check form submission

  const handleCheck = async (e) => {
    e.preventDefault()
    if (!password.trim()) return
    setLoading(true)
    try {
      const res  = await fetch(`${API}/analyze-password`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ password }),
      })
      const data = await res.json()
      setResult(data)
      setGeneratedPwd(generateStrongPassword())
    } catch (err) {
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedPwd)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handlePersonalCheck = async () => {
    const hasInput = Object.values(personalInfo).some(v => v.trim() !== '')
    if (!hasInput) return
    setPersonalLoading(true)
    try {
      const res  = await fetch(`${API}/personal-candidates`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(personalInfo),
      })
      const data = await res.json()
      setPersonalResults(data.candidates)
    } catch (err) {
      console.error('Error:', err)
    } finally {
      setPersonalLoading(false)
    }
  }

  const updatePersonal = (field) => (e) =>
    setPersonalInfo(prev => ({ ...prev, [field]: e.target.value }))

  // calculate bar percentage and color based on strength

  const barPct   = result ? (STRENGTH_PERCENT[result.strength] ?? 0) : 0
  const barColor = result ? (STRENGTH_COLOR[result.strength]   ?? '#888') : '#888'

 //render 

  return (
    <>
    <EyeField count={8} />
    <section id="center">
      <div className="hero">
        <img src={heroImg} alt="" />
      </div>

      <h1>Password Strength Checker</h1>

      {/* ── Input form ── */}
      <form className="input-row" onSubmit={handleCheck}>
        <div className="input-wrapper">
          <input
            type={showPassword ? 'text' : 'password'}
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            type="button"
            className="eye-btn"
            onClick={() => setShowPassword(v => !v)}
            aria-label="Toggle visibility"
          >
            {showPassword ? <img src="/eye.png" alt="Hide password" style={{ width: '16px', height: '16px' }} /> : '🙈'}
          </button>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Checking…' : 'Check'}
        </button>
      </form>

      {/* ── Result card ── */}
      {result && (
        <div className="result-card">

          <div className="card-header">
            <h2>Analysis</h2>
            <span className={`strength ${STRENGTH_CLASS[result.strength]}`}>
              {result.strength}
            </span>
          </div>

          {/* Entropy bar */}
          <div>
            <div className="entropy-bar-track">
              <div
                className="entropy-bar-fill"
                style={{ width: `${barPct}%`, background: barColor }}
              />
            </div>
            <div className="bar-tier-labels">
              <span>Very Weak</span>
              <span>Weak</span>
              <span>Fair</span>
              <span>Strong</span>
              <span>Very Strong</span>
            </div>
          </div>
          <p className="entropy-label">{result.entropy} bits of entropy</p>

          <hr className="divider" />

          {/* Suggestions */}
          {result.issues.length > 0 && (
            <>
              <div>
                <p className="section-label">Suggestions</p>
                <ul className="issues-list">
                  {result.issues.map((issue, i) => (
                    <li key={i} className="issue-item">
                      <span className="issue-dot" />
                      Your password should {issue}
                    </li>
                  ))}
                </ul>
              </div>
              <hr className="divider" />
            </>
          )}

          {/* Crack time */}
          <div>
            <p className="section-label">Estimated crack time</p>
            <div className="crack-times">
              {result.crack_time.map((item, i) => (
                <div key={i} className="crack-card">
                  <p className="crack-type">{item.attack_type}</p>
                  <p className="crack-time-val">{item.time}</p>
                </div>
              ))}
            </div>
          </div>

          <hr className="divider" />

          {/* Password generator */}
          <div>
            <p className="section-label">Suggested stronger password</p>
            <div className="copy-row">
              <code className="generated-pwd">{generatedPwd}</code>
              <button type="button" className="copy-btn" onClick={handleCopy}>
                {copied ? '✓ Copied' : 'Copy'}
              </button>
            </div>
            <p className="gen-hint">Generated locally — never sent anywhere</p>
          </div>

        </div>
      )}

      {/* ── Personal info simulator ── */}
      <div className="personal-section">
        <button
          type="button"
          className="toggle-personal-btn"
          onClick={() => setShowPersonalForm(v => !v)}
        >
          {showPersonalForm
            ? '▲ Hide attack simulator'
            : '▼ See how attackers use your personal info'}
        </button>

        {showPersonalForm && (
          <div className="personal-card">
            <h2>Personal Info Attack Simulator</h2>
            <p className="personal-desc">
              Attackers don't only brute-force passwords, they build targeted wordlists
              from personal information found on social media or in data breaches. Fill
              in any fields below to see what an attacker who knows you might try.
            </p>

            <div className="personal-form">
              <label>
                First name
                <input type="text" placeholder="e.g. Nick"
                  value={personalInfo.first_name} onChange={updatePersonal('first_name')} />
              </label>
              <label>
                Last name
                <input type="text" placeholder="e.g. Smith"
                  value={personalInfo.last_name} onChange={updatePersonal('last_name')} />
              </label>
              <label>
                Birthday
                <input type="date"
                  value={personalInfo.birthdate} onChange={updatePersonal('birthdate')} />
              </label>
              <label>
                Pet / child name
                <input type="text" placeholder="e.g. Buddy"
                  value={personalInfo.pet_name} onChange={updatePersonal('pet_name')} />
              </label>
              <label>
                City / hometown
                <input type="text" placeholder="e.g. Athens"
                  value={personalInfo.city_name} onChange={updatePersonal('city_name')} />
              </label>
            </div>

            <button
              type="button"
              className="analyze-personal-btn"
              onClick={handlePersonalCheck}
              disabled={personalLoading}
            >
              {personalLoading ? 'Generating…' : 'Show attack candidates'}
            </button>

            {personalResults.length > 0 && (
              <div className="personal-results">
                <p className="section-label" style={{ marginBottom: '10px' }}>
                  {personalResults.length} passwords an attacker might try
                </p>
                {personalResults.map((r, i) => (
                  <div key={i} className="personal-result-row">
                    <div className="personal-result-left">
                      <code className="personal-pwd">{r.password}</code>
                      <span className="personal-reason">{r.reason}</span>
                    </div>
                    <div className="personal-result-right">
                      <span className={`strength ${STRENGTH_CLASS[r.strength]}`}
                        style={{ fontSize: '12px' }}>
                        {r.strength}
                      </span>
                      <span className="personal-entropy">{r.entropy} bits</span>
                      <span className="personal-crack">
                        GPU: {r.crack_time.find(c => c.attack_type === 'gpu')?.time}
                      </span>
                    </div>
                  </div>
                ))}
                <p className="personal-warning">
                  ⚠️ If any of these resemble passwords you currently use, change them immediately.
                  None of this data is stored or sent anywhere beyond your local server.
                </p>
              </div>
            )}
          </div>
        )}
      </div>

    </section>
  </>
  )
}