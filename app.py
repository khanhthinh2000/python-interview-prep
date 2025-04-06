from flask import Flask, request, render_template, jsonify
import os
import ast
import pprint
from utils.code_executor import execute_code

app = Flask(__name__)

# Load problems from Python file
from problems import problems

# Load or initialize execution history from history.py
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'history.py')
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, encoding='utf-8') as f:
        content = f.read()
        try:
            start = content.index("[")
            end = content.rindex("]") + 1
            execution_history = ast.literal_eval(content[start:end])
        except Exception:
            execution_history = []
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

        if problem_id not in attempts_remaining:
            attempts_remaining[problem_id] = 2
            success_status[problem_id] = False

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

        result = execute_code(user_code, user_input)
        expected_output = str(problems[problem_id]["expected_output"])
        passed = (str(result["output"]).strip() == expected_output.strip())

        attempts_remaining[problem_id] -= 1
        status = "✅ Success" if passed else "❌ Fail"

        if passed:
            success_status[problem_id] = True

        execution_history.append({
            "code": user_input,
            "output": result["output"],
            "status": status
        })

        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            f.write("execution_history = [\n")
            for entry in execution_history:
                f.write(f"    {entry},\n")
            f.write("]\n")

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
