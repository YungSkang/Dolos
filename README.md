# Dolos

A web-based cybersecurity tool that analyzes password strength and detects potential phising attack risks using rule-based logic and data-driven insights on your emails.

## 🚀 Features

### 🔑 Password Strength Analysis
- Evaluates password based on:
  - Length
  - Uppercase & lowercase characters
  - Digits
  - Special characters
  - Detects common/compromised passwords using a large dataset
- Provides:
  - Strength score (0–100)
  - Classification (Weak / Medium / Strong)
  - Issues and suggestions for improvement

### 🧠 Security Insights (Planned)
- Entropy calculation
- Estimated password cracking time
- Phishing detection (email/URL analysis)

---

## 🛠️ Tech Stack

- **Backend:** Python
- **Data Processing:** CSV dataset (Top 10 Million Passwords)
- **Planned:**
  - FastAPI (API development)
  - React + Tailwind (Frontend dashboard)

---

## 📂 Project Structure
/backend # Python backend logic
/frontend # React frontend (coming soon)
README.md
---

## ⚙️ How It Works

1. User inputs a password
2. System analyzes:
   - Character diversity
   - Length and complexity
   - Presence in known password datasets
3. Returns:
   - Security score
   - Risk level
   - Improvement suggestions

---

## 📊 Example Output
{
    "password": "Test123",
    "score": 60,
    "strength": "Medium",
    "issues": [
        "be longer",
        "contain at least one special character"
    ],
    "suggestions": [
        "Increase complexity and avoid predictable patterns."
    ]
}
---

## 🎯 Future Improvements

- Add entropy-based strength calculation
- Estimate brute-force cracking time
- Implement phishing detection module
- Build interactive dashboard UI
- Deploy as a full-stack web application

---

## 📌 Goal

This project aims to simulate a real-world cybersecurity tool by combining:
- Secure coding practices
- Data-driven analysis
- User-friendly interface design

---

## 👤 Author

Angelos Skandalis  
Informatics & Computer Engineer