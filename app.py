import os
from flask import Flask, render_template, request, jsonify, session
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "chatbot-secret-key-2024"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = "You are a helpful, friendly AI assistant. Be concise and clear in your responses."

@app.route("/")
def index():
    session["messages"] = []
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    if "messages" not in session:
        session["messages"] = []

    messages = session["messages"]
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            max_tokens=1024,
            temperature=0.7,
        )
        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        session["messages"] = messages

        return jsonify({"response": assistant_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/clear", methods=["POST"])
def clear():
    session["messages"] = []
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
