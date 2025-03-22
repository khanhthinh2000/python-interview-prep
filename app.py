from flask import Flask, request, render_template, jsonify
from utils.code_executor import execute_code

app = Flask(__name__)

executions = []  # ✅ Stores all executed code and outputs

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.json
        user_code = data["code"]
        user_input = data.get("userInput", "")

        result = execute_code(user_code, user_input)

        # ✅ Store execution in history
        executions.append({"code": user_code, "output": result["output"]})

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "Error", "output": str(e)})

@app.route("/history")
def history():
    return jsonify(executions)  # ✅ Send stored executions

if __name__ == "__main__":
    app.run(debug=True)
