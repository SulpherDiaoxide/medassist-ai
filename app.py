from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Get Groq API Key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ Please set your GROQ_API_KEY environment variable")

client = Groq(api_key=GROQ_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    prompt = f"""
    User symptoms: {user_input}

    Please provide:
    1. Possible conditions (not a diagnosis)
    2. Recommended medical tests
    3. Urgency level (Low/Medium/High)
    4. Reminder: This is not medical advice, consult a doctor.
    """

    # ✅ FIXED MODEL NAME
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are MedAssist AI, a medical helper (not a doctor)."},
            {"role": "user", "content": prompt}
        ]
    )

    ai_reply = response.choices[0].message.content
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)
