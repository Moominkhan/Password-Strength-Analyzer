from flask import Flask, render_template, request
import re
import math
import random
import string

app = Flask(__name__)

def check_password_strength(password):
    score = 0

    # Length
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1

    # Number
    if re.search(r"\d", password):
        score += 1

    # Special Character
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    # Entropy Calculation
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"\d", password):
        charset += 10

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    entropy = len(password) * math.log2(charset) if charset > 0 else 0

    return score, entropy


def generate_strong_password(length=16):
    characters = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        "!@#$%^&*"
    )

    return ''.join(random.choice(characters) for _ in range(length))


@app.route("/", methods=["GET", "POST"])
def index():

    result = ""
    score = 0
    entropy = 0
    color = ""
    suggestion = ""
    trophy = ""

    suggestions = []
    recommended_password = ""

    if request.method == "POST":

        password = request.form["password"]

        score, entropy = check_password_strength(password)

        # Missing Requirements
        if not re.search(r"[A-Z]", password):
            suggestions.append("Add at least one uppercase letter")

        if not re.search(r"[a-z]", password):
            suggestions.append("Add at least one lowercase letter")

        if not re.search(r"\d", password):
            suggestions.append("Add at least one number")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            suggestions.append("Add at least one special character")

        if len(password) < 12:
            suggestions.append("Increase password length to 12+ characters")

        # Password Rating
        if score <= 2:
            result = "Weak Password"
            color = "weak"
            trophy = "🥉"
            suggestion = "Your password is vulnerable."

        elif score <= 4:
            result = "Medium Password"
            color = "medium"
            trophy = "🥈"
            suggestion = "Improve password security."

        else:
            result = "Strong Password"
            color = "strong"
            trophy = "🏆"
            suggestion = "Excellent password security!"

        # Generate recommendation if not perfect
        if score < 6:
            recommended_password = generate_strong_password()

    return render_template(
        "index.html",
        result=result,
        score=score,
        entropy=round(entropy, 2),
        color=color,
        suggestion=suggestion,
        trophy=trophy,
        suggestions=suggestions,
        recommended_password=recommended_password
    )


if __name__ == "__main__":
    app.run(debug=True)