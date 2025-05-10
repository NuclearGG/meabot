from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from any origin (for frontend communication)

# Your chatbot logic here
def get_bot_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input:
        return "Hi there! How can I assist you today?"
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"
    elif "help" in user_input:
        return "Sure! I'm here to help. Ask anything."
    else:
        return "Sorry, I didn't understand that."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "")
    response = get_bot_response(user_input)
    return jsonify({"reply": response})

if __name__ == '__main__':
    app.run()
