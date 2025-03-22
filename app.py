from flask import Flask, request, render_template, jsonify
import json
import os
from utils.code_executor import execute_code

app = Flask(__name__)

# Load problems from JSON file
PROBLEMS_FILE = os.path.join(os.path.dirname(__file__), 'problems.json')
with open(PROBLEMS_FILE) as f:
    problems = json.load(f)

# Store history in memory for now
execution_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/problems")
def get_problems():
    return jsonify(problems)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    user_code = data["code"]
    user_input = data.get("userInput", "")
    problem_id = data.get("problemId", "1")

    result = execute_code(user_code, problem_id, user_input)

    execution_history.append({
        "code": user_code,
        "output": result["output"]
    })

    return jsonify(result)

@app.route("/history")
def history():
    return jsonify(execution_history)

if __name__ == "__main__":
    app.run(debug=True)
