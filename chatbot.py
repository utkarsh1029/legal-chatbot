from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Google Gemini API
api_key = "AIzaSyAqvZ5wuoVT6M7op77FUs6zF20JEDAaDzs"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Define the model
generation_config = {
    "temperature": 0.15,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="Provide legal assistance based on Indian laws. Ignore irrelevant queries.make precise and shorter replies. only important answer is needed in a well presented way.",
)

chat_session = model.start_chat(history=[])


@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot API requests from frontend."""
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = chat_session.send_message(user_message)
    return jsonify({"response": response.text})


if __name__ == "__main__":
    app.run(debug=True)