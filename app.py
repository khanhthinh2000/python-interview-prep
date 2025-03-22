from flask import Flask, request, render_template, jsonify
import json
import os
from utils.code_executor import execute_code

app = Flask(__name__)

# Load problems from JSON file
PROBLEMS_FILE = os.path.join(os.path.dirname(__file__), 'problems.json')
with open(PROBLEMS_FILE) as f:
    problems = json.load(f)

# Load or initialize execution history
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'history.json')
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE) as f:
        execution_history = json.load(f)
else:
    execution_history = []

# Store attempt count and success flags in memory
attempts_remaining = {}
success_status = {}

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

        # Initialize if first attempt
        if problem_id not in attempts_remaining:
            attempts_remaining[problem_id] = 2
            success_status[problem_id] = False

        # If already successful or attempts exhausted
        if success_status[problem_id]:
            return jsonify({
                "output": "Already completed successfully.",
                "status": "completed",
                "attempts": attempts_remaining[problem_id]
            })

        if attempts_remaining[problem_id] <= 0:
            return jsonify({
                "output": "No attempts remaining. Try another one.",
                "status": "locked",
                "attempts": 0
            })

        # Run the code
        result = execute_code(user_code, user_input)
        expected_output = str(problems[problem_id]["expected_output"])
        passed = (str(result["output"]).strip() == expected_output.strip())

        attempts_remaining[problem_id] -= 1
        status = "✅ Success" if passed else "❌ Fail"

        if passed:
            success_status[problem_id] = True

        # Save to execution history and persist it
        execution_history.append({
            "code": user_input,
            "output": result["output"],
            "status": status
        })

        with open(HISTORY_FILE, 'w') as f:
            json.dump(execution_history, f, indent=4)

        return jsonify({
            "output": result["output"],
            "status": status,
            "attempts": attempts_remaining[problem_id],
            "completed": passed
        })

    except Exception as e:
        return jsonify({
            "output": f"Error: {str(e)}",
            "status": "❌ Fail"
        }), 500

@app.route("/history")
def history():
    return jsonify(execution_history)

if __name__ == "__main__":
    app.run(debug=True)
