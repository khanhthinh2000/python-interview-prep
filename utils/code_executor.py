import sys
import io
import re

def execute_code(user_code, user_input):
    """
    Executes user-submitted Python code in a safe environment.

    Args:
        user_code (str): The Python code submitted by the user.
        user_input (str): Function arguments entered by the user.

    Returns:
        dict: A dictionary containing execution status and output.
    """
    safe_globals = {}

    try:
        output_buffer = io.StringIO()
        sys.stdout = output_buffer  # Redirect print output

        # ✅ Execute user-defined Python code
        exec(user_code, safe_globals)

        # ✅ Check if the code contains a function
        function_match = re.search(r"def (\w+)\(", user_code)
        if function_match:
            function_name = function_match.group(1)

            if function_name in safe_globals:
                # ✅ Execute function with user arguments if provided
                if user_input:
                    parsed_args = eval(f"({user_input},)")
                    result = safe_globals[function_name](*parsed_args)
                else:
                    result = safe_globals[function_name]()
            else:
                result = "Function not found."
        else:
            result = ""

        sys.stdout = sys.__stdout__  # Restore stdout
        printed_output = output_buffer.getvalue().strip()

        final_output = printed_output + (f"\n{result}" if result else "")
        return {"status": "Success", "output": final_output.strip()}

    except Exception as e:
        sys.stdout = sys.__stdout__
        return {"status": "Error", "output": str(e)}
