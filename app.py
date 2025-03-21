# from flask import Flask, request, render_template, jsonify

# app = Flask(__name__)

# # Load problems from JSON file
# import json
# with open("problems.json") as f:
#     problems = json.load(f)

# @app.route("/")
# def home():
#     return render_template("index.html", problem=problems["1"])

# @app.route("/submit", methods=["POST"])
# def submit():
#     data = request.json
#     user_code = data["code"]

#     # Safe execution environment
#     safe_globals = {}

#     try:
#         exec(user_code, safe_globals)
#         if "sum_two_numbers" in safe_globals:
#             result = safe_globals["sum_two_numbers"](2, 3)  # Execute function with test inputs
#         else:
#             result = "Function not found"

#         expected = problems["1"]["expected_output"]
#         status = "Correct" if str(result).strip() == str(expected).strip() else "Incorrect"

#         return jsonify({
#             "status": status,
#             "output": str(result),
#             "expected": str(expected)  # Debugging: Show expected output
#         })
#     except Exception as e:
#         return jsonify({"status": "Error", "error": str(e)})

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, render_template, jsonify
from utils.code_executor import execute_code
from utils.feedback import provide_feedback  # Import feedback function
import json

app = Flask(__name__)

# Load problems from JSON
with open("problems.json") as f:
    problems = json.load(f)

@app.route("/")
def home():
    return render_template("index.html", problem=problems["1"])

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    user_code = data["code"]
    problem_id = "1"

    result = execute_code(user_code, problem_id)

    # Add feedback if incorrect
    if result["status"] == "Incorrect":
        result["feedback"] = provide_feedback(result["output"], result["expected"])

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
