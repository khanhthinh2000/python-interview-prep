import unittest
from utils.code_executor import execute_code

class TestCodeExecutor(unittest.TestCase):

    def test_correct_solution(self):
        user_code = "def sum_two_numbers(a, b): return a + b\nresult = sum_two_numbers(2, 3)"
        result = execute_code(user_code, "1")
        self.assertEqual(result["status"], "Correct")

    def test_incorrect_solution(self):
        user_code = "def sum_two_numbers(a, b): return a - b\nresult = sum_two_numbers(2, 3)"
        result = execute_code(user_code, "1")
        self.assertEqual(result["status"], "Incorrect")

    def test_syntax_error(self):
        user_code = "def sum_two_numbers(a, b return a + b\nresult = sum_two_numbers(2, 3)"
        result = execute_code(user_code, "1")
        self.assertEqual(result["status"], "Error")

if __name__ == "__main__":
    unittest.main()
