"""
AI Resume & Job Matcher — Flask Application
"""

import os
import io
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from nlp_matcher import analyze_match

# ─── Try importing PDF reader (optional) ──────────────────────────────────────
try:
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from docx import Document
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

# ─── App Configuration ─────────────────────────────────────────────────────────
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024   # 5 MB
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_file(file) -> str:
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    raw = file.read()

    if ext == 'txt':
        return raw.decode('utf-8', errors='ignore')

    if ext == 'pdf':
        if PDF_SUPPORT:
            with pdfplumber.open(io.BytesIO(raw)) as pdf:
                return '\n'.join(
                    page.extract_text() or '' for page in pdf.pages
                )
        return ''

    if ext == 'docx':
        if DOCX_SUPPORT:
            doc = Document(io.BytesIO(raw))
            return '\n'.join(p.text for p in doc.paragraphs)
        return ''

    return ''


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html', pdf_support=PDF_SUPPORT, docx_support=DOCX_SUPPORT)


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # ── Get Resume text ──────────────────────────────────────────────────
        resume_text = ''
        if 'resume_file' in request.files and request.files['resume_file'].filename:
            f = request.files['resume_file']
            if allowed_file(f.filename):
                resume_text = extract_text_from_file(f)
        if not resume_text:
            resume_text = request.form.get('resume_text', '').strip()

        # ── Get Job Description ──────────────────────────────────────────────
        job_text = request.form.get('job_text', '').strip()

        # ── Validation ───────────────────────────────────────────────────────
        if not resume_text:
            return jsonify({'error': 'Please provide your resume (paste text or upload a file).'}), 400
        if not job_text:
            return jsonify({'error': 'Please paste the job description.'}), 400
        if len(resume_text) < 50:
            return jsonify({'error': 'Resume text seems too short. Please add more content.'}), 400
        if len(job_text) < 50:
            return jsonify({'error': 'Job description seems too short.'}), 400

        # ── Run NLP Analysis ─────────────────────────────────────────────────
        result = analyze_match(resume_text, job_text)
        return jsonify({'success': True, 'data': result})

    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'pdf_support': PDF_SUPPORT, 'docx_support': DOCX_SUPPORT})


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n🚀  AI Resume Matcher is running at http://127.0.0.1:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
