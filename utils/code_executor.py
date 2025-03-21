import json

def execute_code(user_code, problem_id):
    """
    Executes user-submitted Python code in a safe environment.
    
    Args:
        user_code (str): The Python code submitted by the user.
        problem_id (str): The ID of the problem being solved.
    
    Returns:
        dict: A dictionary containing the execution status, output, and expected output.
    """
    # Load problems from JSON
    with open("problems.json") as f:
        problems = json.load(f)

    if problem_id not in problems:
        return {"status": "Error", "output": "Problem not found"}

    expected = problems[problem_id]["expected_output"]
    
    # Safe execution environment
    safe_globals = {}

    try:
        exec(user_code, safe_globals)
        
        if "result" in safe_globals:
            result = safe_globals["result"]
        else:
            return {"status": "Error", "output": "No result variable found"}

        status = "Correct" if str(result).strip() == str(expected).strip() else "Incorrect"
        return {"status": status, "output": str(result), "expected": str(expected)}
    
    except Exception as e:
        return {"status": "Error", "output": str(e)}
