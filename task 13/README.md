# ResumeIQ — AI Resume & Job Matcher

An NLP-powered Flask web application that analyzes how well your resume matches a job description.

## ✨ Features

- **TF-IDF Semantic Matching** — Measures overall content similarity using term frequency analysis
- **Keyword Overlap Detection** — Identifies matching vocabulary between resume and job post
- **Technical Skills Extraction** — Matches 100+ tech skills (Python, AWS, React, ML, etc.)
- **Soft Skills Analysis** — Detects communication, leadership, teamwork, and more
- **Gap Analysis** — Shows exactly which skills are missing
- **Actionable Recommendations** — Specific tips to improve your match score
- **File Upload Support** — Accepts PDF, DOCX, and TXT resumes

## 🚀 Quick Start

### 1. Clone / Extract the project

```bash
cd resume_matcher
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000
```

## 📁 Project Structure

```
resume_matcher/
├── app.py              # Flask routes & file handling
├── nlp_matcher.py      # NLP engine (TF-IDF, skill extraction, scoring)
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Full-stack UI (HTML/CSS/JS)
├── uploads/            # Temp storage for uploaded files
└── README.md
```

## 🧠 How the Scoring Works

| Component         | Weight | Description                                |
|-------------------|--------|--------------------------------------------|
| Semantic (TF-IDF) | 40%    | Overall language & content similarity      |
| Keyword Overlap   | 25%    | Matching important words                   |
| Technical Skills  | 25%    | Known tech skill dictionary matching       |
| Soft Skills       | 10%    | Leadership, communication, teamwork, etc.  |

**Score Grades:**
- 🟢 80–100% — Excellent Match
- 🔵 60–79%  — Good Match
- 🟡 40–59%  — Partial Match
- 🔴 0–39%   — Weak Match

## 🛠 Tech Stack

- **Backend:** Flask, NLTK, scikit-learn
- **NLP:** TF-IDF Vectorizer, Cosine Similarity, Lemmatization
- **File Parsing:** pdfplumber (PDF), python-docx (DOCX)
- **Frontend:** Vanilla HTML/CSS/JS with animated UI

## 💡 Tips for Best Results

1. Paste the **complete** job description including requirements section
2. Include your **full resume** with all skills, experience, and education
3. Use the **missing skills** list to tailor your resume keywords
4. Aim for **60%+ score** before applying
