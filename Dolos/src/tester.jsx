import { useState } from 'react'
import heroImg from './assets/hero.png'
import './App.css'

// --- Helpers ---

const strengthToPercent = {
  "Compromised": 5,
  "Very Weak":   15,
  "Weak":        35,
  "Fair":        60,
  "Strong":      85,
  "Very Strong": 100,
}

const strengthToColor = {
  "Compromised": "#ff0000",
  "Very Weak":   "#ff4500",
  "Weak":        "#ff8c00",
  "Fair":        "#ffd700",
  "Strong":      "#7cfc00",
  "Very Strong": "#00ff9f",
}

const strengthClass = {
  "Compromised": "compromised",
  "Very Weak":   "very-weak",
  "Weak":        "weak",
  "Fair":        "fair",
  "Strong":      "strong",
  "Very Strong": "very-strong",
}

// Generate a random strong password client-side
function generateStrongPassword(length = 14) {
  const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-='
  const array = new Uint8Array(length)
  crypto.getRandomValues(array)
  return Array.from(array).map(b => charset[b % charset.length]).join('')
}

// Build personal info based passwords an attacker might try
function buildPersonalPasswords(info) {
  const { firstName, lastName, birthdate, petName, cityName } = info

  const results = []

  const bd = birthdate ? new Date(birthdate) : null
  const day   = bd ? String(bd.getDate()).padStart(2, '0') : null
  const month = bd ? String(bd.getMonth() + 1).padStart(2, '0') : null
  const year2 = bd ? String(bd.getFullYear()).slice(2) : null
  const year4 = bd ? String(bd.getFullYear()) : null

  const cap = s => s ? s.charAt(0).toUpperCase() + s.slice(1).toLowerCase() : null

  const add = (pass, reason) => {
    if (pass && pass.length >= 4) results.push({ password: pass, reason })
  }

  if (firstName) {
    add(cap(firstName), 'First name alone')
    if (year2) add(`${cap(firstName)}${year2}`, 'First name + birth year (2 digit)')
    if (year4) add(`${cap(firstName)}${year4}`, 'First name + birth year (4 digit)')
    if (month && day) add(`${cap(firstName)}${day}${month}`, 'First name + birth day/month')
    if (month && year2) add(`${cap(firstName)}${month}${year2}`, 'First name + month + short year')
    if (day && month && year2) add(`${cap(firstName)}${day}${month}${year2}`, 'First name + full date')
  }

  if (lastName) {
    add(cap(lastName), 'Last name alone')
    if (year4) add(`${cap(lastName)}${year4}`, 'Last name + birth year')
    if (firstName) add(`${cap(firstName)}${cap(lastName)}`, 'Full name combined')
    if (firstName && year2) add(`${cap(firstName)}.${cap(lastName)}${year2}`, 'Name.Surname + year')
  }

  if (petName) {
    add(cap(petName), 'Pet name alone')
    if (year2) add(`${cap(petName)}${year2}`, 'Pet name + year')
    if (day && month) add(`${cap(petName)}${day}${month}`, 'Pet name + birthday')
    if (firstName) add(`${cap(firstName)}${cap(petName)}`, 'First name + pet name')
  }

  if (cityName) {
    add(cap(cityName), 'City name alone')
    if (year4) add(`${cap(cityName)}${year4}`, 'City + birth year')
    if (firstName) add(`${cap(firstName)}${cap(cityName)}`, 'First name + city')
  }

  if (birthdate) {
    if (day && month && year4) add(`${day}/${month}/${year4}`, 'Full date dd/mm/yyyy')
    if (day && month && year2) add(`${day}${month}${year2}`, 'Compact date ddmmyy')
    if (year4) add(year4, 'Birth year alone')
  }

  return results
}


// --- Component ---

export default function App() {
  const [password, setPassword]       = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [result, setResult]           = useState(null)
  const [loading, setLoading]         = useState(false)
  const [copied, setCopied]           = useState(false)
  const [generatedPwd, setGeneratedPwd] = useState(() => generateStrongPassword())
  const [showPersonalForm, setShowPersonalForm] = useState(false)

  const [personalInfo, setPersonalInfo] = useState({
    firstName: '', lastName: '', birthdate: '', petName: '', cityName: ''
  })
  const [personalResults, setPersonalResults] = useState([])
  const [personalLoading, setPersonalLoading] = useState(false)

  const handleCheck = async (e) => {
    e.preventDefault()
    if (!password.trim()) return
    setLoading(true)
    try {
      const response = await fetch('http://127.0.0.1:8000/analyze-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      })
      const data = await response.json()
      setResult(data)
      setGeneratedPwd(generateStrongPassword())
    } catch (error) {
      console.error('Error:', error)
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
    const candidates = buildPersonalPasswords(personalInfo)
    if (candidates.length === 0) return
    setPersonalLoading(true)

    try {
      const checked = await Promise.all(
        candidates.map(async ({ password: pwd, reason }) => {
          const res = await fetch('http://127.0.0.1:8000/analyze-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: pwd })
          })
          const data = await res.json()
          return { password: pwd, reason, strength: data.strength, entropy: data.entropy, crack_time: data.crack_time }
        })
      )
      setPersonalResults(checked)
    } catch (err) {
      console.error(err)
    } finally {
      setPersonalLoading(false)
    }
  }

  const pct = result ? (strengthToPercent[result.strength] ?? 0) : 0
  const col = result ? (strengthToColor[result.strength] ?? '#888') : '#888'

  return (
    <section id="center">

      <div className="hero">
        <img src={heroImg} alt="" />
      </div>

      <h1>Password Strength Checker</h1>

      {/* Input form */}
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
            {showPassword ? '🙈' : '👁'}
          </button>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Checking…' : 'Check'}
        </button>
      </form>

      {/* Result card */}
      {result && (
        <div className="result-card">

          {/* Header row */}
          <div className="card-header">
            <h2>Analysis</h2>
            <span className={`strength ${strengthClass[result.strength]}`}>
              {result.strength}
            </span>
          </div>

          {/* Entropy bar */}
          <div>
            <div className="entropy-bar-track">
              <div
                className="entropy-bar-fill"
                style={{ width: `${pct}%`, background: col }}
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
          )}

          {result.issues.length > 0 && <hr className="divider" />}

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

      {/* Personal info section */}
      <div className="personal-section">
        <button
          type="button"
          className="toggle-personal-btn"
          onClick={() => setShowPersonalForm(v => !v)}
        >
          {showPersonalForm ? '▲ Hide' : '▼ See how attackers use your personal info'}
        </button>

        {showPersonalForm && (
          <div className="personal-card">
            <h2>Personal Info Attack Simulator</h2>
            <p className="personal-desc">
              In real-world attacks, people craft password guesses from publicly available personal
              information — social media, data breaches, or simply knowing you. Fill in any fields
              below to see what an attacker might try against you.
            </p>

            <div className="personal-form">
              <label>First name
                <input
                  type="text" placeholder="e.g. Nick"
                  value={personalInfo.firstName}
                  onChange={e => setPersonalInfo(p => ({ ...p, firstName: e.target.value }))}
                />
              </label>
              <label>Last name
                <input
                  type="text" placeholder="e.g. Smith"
                  value={personalInfo.lastName}
                  onChange={e => setPersonalInfo(p => ({ ...p, lastName: e.target.value }))}
                />
              </label>
              <label>Birthday
                <input
                  type="date"
                  value={personalInfo.birthdate}
                  onChange={e => setPersonalInfo(p => ({ ...p, birthdate: e.target.value }))}
                />
              </label>
              <label>Pet / child name
                <input
                  type="text" placeholder="e.g. Buddy"
                  value={personalInfo.petName}
                  onChange={e => setPersonalInfo(p => ({ ...p, petName: e.target.value }))}
                />
              </label>
              <label>City / hometown
                <input
                  type="text" placeholder="e.g. Athens"
                  value={personalInfo.cityName}
                  onChange={e => setPersonalInfo(p => ({ ...p, cityName: e.target.value }))}
                />
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
                      <span className={`strength ${strengthClass[r.strength]}`} style={{ fontSize: '12px' }}>
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
                  ⚠️ If any of these resemble passwords you use, change them immediately.
                  This data never leaves your browser.
                </p>
              </div>
            )}
          </div>
        )}
      </div>

    </section>
  )
}