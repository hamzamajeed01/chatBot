from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

API_KEY = "AIzaSyDA4QrmzBxO2BPv9oGRoA0-dSTV9_Bi-wY"
app = Flask(__name__)
CORS(app)
genai.configure(api_key=API_KEY)

generationConfig = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generationConfig,
    system_instruction="You will act as AI assistance and answer the questions being asked.",
)

chatSession = model.start_chat(history=[])

@app.route('/ask', methods=['POST'])
def askQuestion():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"success": False, "error": "No question provided"})
    
    try:
        response = chatSession.send_message(question)
        answer = response.text if response.text else 'No answer generated.'
        return jsonify({"success": True, "answer": answer})
    except Exception as e:
        return jsonify({"success": False, "error": f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')