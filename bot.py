from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import csv
import string
import random

# Load CSV data into a dictionary




app = Flask(__name__)

CORS(app, origin='127.0.0.1:1306')

translator = str.maketrans('','',string.punctuation)
greetings = ['hey','howda','howdy','hello','hi',"whats up"]
chat_end = ["bye","exit0","exit","goodbye"]
greeting_responses = [
    "Hello there, I am MEA bot and I shall assist you about knowing the school, the syllabus, etc. I'll try my best to assist you.",
    "Hi! I'm MEA bot. How can I help you today regarding the school or syllabus?",
    "Greetings! As MEA bot, I'm here to provide information about the school and its syllabus."
]
farewell_responses = [
    "Thank You! Bye",
    "Goodbye! Have a great day!",
    "See you later! Feel free to ask if you have more questions."
]
easterpair = {}
qa_pairs = {}
with open("easter.csv", newline='', encoding='utf-8') as easter:
    reader = csv.DictReader(easter)
    for row in reader:
        code = row["code"].strip().lower()
        easter = row['easter'].strip()
        easterpair[code] = easter
with open("mea-bot-compiled.csv", newline='', encoding='utf-8') as basic:
    reader = csv.DictReader(basic)
    for row in reader:
        question = row["question"].strip().lower()
        answer = row["answer"].strip()
        qa_pairs[question] = answer# Allow requests from any origin (for frontend communication)

# Your chatbot logic here
def get_bot_response(user_input):
    # Normalize user input first
    normalized_user_input = user_input.strip().lower().translate(translator)


    for greet_phrase in greetings:
        if greet_phrase in normalized_user_input:
            return random.choice(greeting_responses)


    for end_phrase in chat_end:
        if end_phrase in normalized_user_input:
            if 'exit' in normalized_user_input: # Check for 'exit' specifically here
                return "EXIT<br>CODE:0<br>EXITING AT CODE 0<br> no error"
            return random.choice(farewell_responses)


    for question, answer in qa_pairs.items():
        # You might want to consider exact match first, then broader matches
        # Or, if you want to allow partial matches:
        if question in normalized_user_input: # If a QA question is part of the user's input
            return answer
    for code, easter in easterpair.items():
        if  normalized_user_input == code:
            return easter


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
