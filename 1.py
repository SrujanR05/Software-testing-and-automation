import unittest

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

class TestCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(10, 5), 15)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)

    def test_multiply(self):
        self.assertEqual(multiply(10, 5), 50)

    def test_divide(self):
        self.assertEqual(divide(10, 5), 2)

if __name__ == "__main__":
    print("Addition =", add(10, 5))
    print("Subtraction =", subtract(10, 5))
    print("Multiplication =", multiply(10, 5))
    print("Division =", divide(10, 5))
    unittest.main()