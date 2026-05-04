"""
NLP Resume & Job Matcher Engine
Uses TF-IDF + Cosine Similarity + Keyword Extraction
"""

import re
import string
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

# Use sklearn's built-in stopwords (no network download needed)
STOP_WORDS = set(ENGLISH_STOP_WORDS)

# ─── Tech & Soft Skills Dictionaries ──────────────────────────────────────────

TECH_SKILLS = {
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go",
    "rust", "php", "swift", "kotlin", "scala", "r", "matlab", "sql", "bash",
    # Web
    "html", "css", "react", "angular", "vue", "node.js", "nodejs", "django",
    "flask", "fastapi", "spring", "express", "next.js", "nextjs", "tailwind",
    # Data/ML/AI
    "machine learning", "deep learning", "nlp", "natural language processing",
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "pandas",
    "numpy", "matplotlib", "seaborn", "opencv", "bert", "gpt", "transformer",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins",
    "ci/cd", "devops", "git", "github", "gitlab", "linux", "unix",
    # Databases
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite",
    "oracle", "cassandra", "dynamodb",
    # Other
    "api", "rest", "graphql", "microservices", "agile", "scrum", "jira",
    "excel", "tableau", "power bi", "spark", "hadoop", "kafka",
}

SOFT_SKILLS = {
    "communication", "leadership", "teamwork", "problem-solving", "creativity",
    "analytical", "critical thinking", "time management", "adaptability",
    "collaboration", "presentation", "negotiation", "mentoring", "project management",
    "decision making", "attention to detail", "multitasking", "organization",
}

# ─── Text Preprocessing ───────────────────────────────────────────────────────

def preprocess_text(text: str) -> str:
    """Clean and normalize text."""
    text = text.lower()
    text = re.sub(r'[^\w\s\.\+\#]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_keywords(text: str) -> list[str]:
    """Extract meaningful keywords using regex tokenization."""
    tokens = re.findall(r'\b[a-z][a-z0-9\.\+\#]*\b', preprocess_text(text))
    keywords = [
        t for t in tokens
        if t not in STOP_WORDS
        and len(t) > 2
        and not t.isdigit()
    ]
    return keywords


def extract_skills(text: str, skill_set: set) -> list[str]:
    """Extract skills from text by matching against a known skill dictionary."""
    text_lower = text.lower()
    found = []
    for skill in skill_set:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return sorted(found)


# ─── Core Matching Engine ─────────────────────────────────────────────────────

def compute_tfidf_similarity(text1: str, text2: str) -> float:
    """Compute TF-IDF cosine similarity between two texts."""
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words='english',
        max_features=5000,
        sublinear_tf=True
    )
    try:
        tfidf_matrix = vectorizer.fit_transform([
            preprocess_text(text1),
            preprocess_text(text2)
        ])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except Exception:
        return 0.0


def compute_keyword_overlap(resume_kws: list, job_kws: list) -> float:
    """Compute keyword overlap score (Jaccard-like)."""
    set1 = set(resume_kws)
    set2 = set(job_kws)
    if not set2:
        return 0.0
    intersection = len(set1 & set2)
    return intersection / len(set2)


def compute_skill_score(resume_skills: list, job_skills: list) -> float:
    """Compute skill match percentage."""
    if not job_skills:
        return 1.0
    matched = set(resume_skills) & set(job_skills)
    return len(matched) / len(job_skills)


# ─── Main Analyzer ────────────────────────────────────────────────────────────

def analyze_match(resume_text: str, job_text: str) -> dict:
    """
    Full analysis pipeline. Returns a rich result dictionary.
    """
    # 1. Extract skills
    resume_tech  = extract_skills(resume_text, TECH_SKILLS)
    job_tech     = extract_skills(job_text,    TECH_SKILLS)
    resume_soft  = extract_skills(resume_text, SOFT_SKILLS)
    job_soft     = extract_skills(job_text,    SOFT_SKILLS)

    # 2. Keywords
    resume_kws = extract_keywords(resume_text)
    job_kws    = extract_keywords(job_text)

    # 3. Scores
    tfidf_score   = compute_tfidf_similarity(resume_text, job_text)
    keyword_score = compute_keyword_overlap(resume_kws, job_kws)
    tech_score    = compute_skill_score(resume_tech, job_tech)
    soft_score    = compute_skill_score(resume_soft, job_soft)

    # 4. Weighted composite score
    composite = (
        tfidf_score   * 0.40 +
        keyword_score * 0.25 +
        tech_score    * 0.25 +
        soft_score    * 0.10
    )
    composite = min(composite * 1.15, 1.0)   # slight boost to avoid pessimism

    # 5. Matched / Missing / Bonus skills
    matched_tech   = sorted(set(resume_tech) & set(job_tech))
    missing_tech   = sorted(set(job_tech)    - set(resume_tech))
    bonus_tech     = sorted(set(resume_tech) - set(job_tech))
    matched_soft   = sorted(set(resume_soft) & set(job_soft))
    missing_soft   = sorted(set(job_soft)    - set(resume_soft))

    # 6. Top resume keywords (most frequent meaningful words)
    kw_freq = Counter(resume_kws)
    top_resume_kws = [w for w, _ in kw_freq.most_common(15) if len(w) > 3]

    # 7. Recommendation label
    pct = composite * 100
    if pct >= 80:
        label, color = "Excellent Match", "green"
    elif pct >= 60:
        label, color = "Good Match", "blue"
    elif pct >= 40:
        label, color = "Partial Match", "yellow"
    else:
        label, color = "Weak Match", "red"

    return {
        "overall_score":    round(pct, 1),
        "label":            label,
        "label_color":      color,
        "scores": {
            "semantic":     round(tfidf_score   * 100, 1),
            "keyword":      round(keyword_score * 100, 1),
            "technical":    round(tech_score    * 100, 1),
            "soft_skills":  round(soft_score    * 100, 1),
        },
        "skills": {
            "matched_tech":  matched_tech,
            "missing_tech":  missing_tech,
            "bonus_tech":    bonus_tech,
            "matched_soft":  matched_soft,
            "missing_soft":  missing_soft,
        },
        "top_resume_keywords": top_resume_kws,
        "recommendations": _build_recommendations(missing_tech, missing_soft, pct),
    }


def _build_recommendations(missing_tech, missing_soft, score):
    recs = []
    if missing_tech:
        top = missing_tech[:5]
        recs.append(f"Add or highlight these technical skills: {', '.join(top)}.")
    if missing_soft:
        recs.append(f"Showcase soft skills like: {', '.join(missing_soft[:3])}.")
    if score < 60:
        recs.append("Tailor your resume language to mirror the job description keywords.")
    if score >= 80:
        recs.append("Strong match! Focus on quantifying your achievements (numbers, %).")
    if not missing_tech and not missing_soft:
        recs.append("Great coverage! Consider adding a strong summary statement.")
    return recs
