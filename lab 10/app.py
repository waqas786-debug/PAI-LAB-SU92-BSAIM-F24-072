from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

KNOWLEDGE_BASE = {
    "requirements": "Minimum 60% in your previous degree is required.",
    "deadline": "The final date to apply for Fall 2026 is August 15th.",
    "programs": "We offer CS, SE, Electrical Engineering, and BBA.",
    "fee": "The average fee is $1500 per semester."
}

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('message', '').lower()
    response = "I am sorry, I don't have information on that. Contact the admin office."
    
    for key in KNOWLEDGE_BASE:
        if key in user_input:
            response = KNOWLEDGE_BASE[key]
            break
            
    return jsonify({"reply": response})

if __name__ == '__main__':
    app.run(debug=True)