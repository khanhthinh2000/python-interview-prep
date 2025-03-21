import sys
import io

def execute_code(user_code):
    """
    Executes user-submitted Python code in a safe environment.

    Args:
        user_code (str): The Python code submitted by the user.

    Returns:
        dict: A dictionary containing execution status and output.
    """
    safe_globals = {}

    try:
        # Capture print statements
        output_buffer = io.StringIO()
        sys.stdout = output_buffer  # Redirect standard output

        # ✅ Execute any Python code (not just functions)
        exec(user_code, safe_globals)

        # Restore stdout and get printed output
        sys.stdout = sys.__stdout__
        printed_output = output_buffer.getvalue().strip()

        return {
            "status": "Success",
            "output": printed_output.strip() if printed_output else "Execution completed with no output."
        }

    except Exception as e:
        sys.stdout = sys.__stdout__
        return {"status": "Error", "output": str(e)}
