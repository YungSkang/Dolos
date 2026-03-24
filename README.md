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
  - Entropy calculation
  - Estimated password cracking time

### 🧠 Security Insights (Planned)
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
    'entropy': 104.87, 
    'crack_time': [
      {'attack_type': 'online', 
      'time': '31,688,087.8 years'},
      {'attack_type': 'offline',
      'time': '31.7 years'}, 
      {'attack_type': 'gpu', 
      'time': '3.2 years'}]
}
---

## 🎯 Future Improvements
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