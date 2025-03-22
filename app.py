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
    try:
        data = request.json
        user_code = data["code"]
        user_input = data.get("userInput", "")
        problem_id = data.get("problemId", "1")

        if problem_id not in problems:
            return jsonify({ "output": f"Error: Problem ID '{problem_id}' not found." }), 400

        print(f"Executing problem {problem_id} with user code:\n{user_code}")
        result = execute_code(user_code, user_input)

        execution_history.append({
            "code": user_code,
            "output": result["output"]
        })

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "output": f"Error: {str(e)}"
        }), 500

@app.route("/history")
def history():
    return jsonify(execution_history)

if __name__ == "__main__":
    app.run(debug=True)
