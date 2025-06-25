from flask import Flask, render_template, request, redirect, url_for
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Available personas
personas = {
    "Friendly Assistant": "You're a helpful and friendly assistant who always answers politely and clearly.",
    "Strict Teacher": "You're a strict but knowledgeable teacher. You explain concepts in a precise, no-nonsense tone.",
    "Motivational Coach": "You're an energetic coach who always encourages and motivates users."
}

app = Flask(__name__)

# Chat history
messages = []
@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        selected_persona = request.form.get("persona", "Friendly Assistant")
        user_input = request.form["user_input"]
        persona_prompt = personas[selected_persona]

        # Combine persona and user input
        full_prompt = f"{persona_prompt}\nUser: {user_input}"

        try:
            model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
            response = model.generate_content(full_prompt)

            messages.append(("user", user_input))
            messages.append(("bot", response.text.strip()))
        except Exception as e:
            messages.append(("error", f"Error: {str(e)}"))

        return redirect(url_for("chat", persona=selected_persona))

    # For GET request (after redirect)
    selected_persona = request.args.get("persona", "Friendly Assistant")
    return render_template("chat.html", messages=messages, personas=personas, selected=selected_persona)

if __name__ == "__main__":
    app.run(debug=True)
