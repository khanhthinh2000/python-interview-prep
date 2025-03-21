from flask import Flask, request, render_template, jsonify
from utils.code_executor import execute_code  # ✅ Updated to execute any code

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # ✅ No longer restricted to functions

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.json
        user_code = data["code"]

        print("DEBUG - Received code:", user_code)  # Debugging log

        result = execute_code(user_code)

        print("DEBUG - API Response:", result)  # Debugging log

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "Error", "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
