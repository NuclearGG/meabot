from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import csv

# Load CSV data into a dictionary




app = Flask(__name__)

CORS(app)
qa_pairs = {}
with open("mea-bot-compiled.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        question = row["Question"].strip().lower()
        answer = row["Answer"].strip()
        qa_pairs[question] = answer# Allow requests from any origin (for frontend communication)

# Your chatbot logic here
def get_bot_response(user_input):
    user_input = user_input.strip().lower()
    for question, answer in qa_pairs.items():
        if question in user_input:
            return answer
    return "Sorry, I didn't understand that. Please ask something else."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "")
    response = get_bot_response(user_input)
    return jsonify({"reply": response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
