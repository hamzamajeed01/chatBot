from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PyPDF2 import PdfReader
import google.generativeai as genai
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize the Gemini API client with your API key
genai.configure(api_key='AIzaSyDA4QrmzBxO2BPv9oGRoA0-dSTV9_Bi-wY')

# Define the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="I will ask questions ; try to answer them perfectly.",
)

# Ensure the uploads directory exists
os.makedirs('uploads', exist_ok=True)

# Initialize global variables
pdf_text = ""
chat_session = model.start_chat(history=[])
@app.route('/')
def index():
    return render_template('index.html')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        pdf_text = ''.join(page.extract_text() for page in reader.pages)
    return pdf_text

@app.route('/upload', methods=['POST'])
def upload_file():
    global pdf_text
    if 'file' not in request.files:
        return jsonify(success=False, error='No file part')

    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, error='No selected file')

    if file:
        # Clear the uploads directory
        for filename in os.listdir('uploads'):
            file_path = os.path.join('uploads', filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

        # Save the new file
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)

        # Load the PDF content
        pdf_text = extract_text_from_pdf(filepath)
        print(pdf_text)

        # Create an initial prompt with the PDF content
        initial_prompt = f"Kindly go through the text which is of a pdf and now I will ask questions and you will answer based on PDF content: if no answer found with respect to pdf text provide a generic answer. PDF Text is: {pdf_text}"
        
        # Add the initial prompt to the chat history
        response = chat_session.send_message(initial_prompt)
        
        try:
            print(response)
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, error=f'An error occurred: {str(e)}')

    return jsonify(success=False, error='Failed to upload file')

@app.route('/ask', methods=['POST'])
def ask_question():
    global chat_history
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify(answer=None, error='No question provided')
    try:
        print(question)
        # Send the entire conversation history to the model
        response = chat_session.send_message(question)
        answer = response.text if response.text else 'No answer generated.'
        print(answer)
        return jsonify(answer=answer)
    except Exception as e:
        return jsonify(answer=None, error=f'An error occurred: {str(e)}')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
