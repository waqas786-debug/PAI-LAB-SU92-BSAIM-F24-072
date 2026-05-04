from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Structured Knowledge Base
CAMPUS_INFO = {
    "apply": "You can apply via our online portal at admissions.university.edu.",
    "programs": "We offer majors in Computer Science, Data Science, and AI.",
    "merit": "The closing merit for CS last year was 82%.",
    "contact": "You can email us at helpdesk@university.edu for queries."
}

@app.route('/')
def index():
    return render_template('bot_interface.html')

@app.route('/process_query', methods=['POST'])
def process_query():
    client_msg = request.json.get('text', '').lower()
    bot_reply = "I'm not sure about that. Would you like to talk to a human counselor?"

    for keyword, detail in CAMPUS_INFO.items():
        if keyword in client_msg:
            bot_reply = detail
            break
            
    return jsonify({"response": bot_reply})

if __name__ == '__main__':
    app.run(port=5050)