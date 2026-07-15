def add_two_numbers(a, b):
    return a + b
def subtract_two_numbers(a, b):
    return a - b
def multiply_two_numbers(a, b):
    return a * b
def divide_two_numbers(a, b):
    return a / b


def test_add_two_numbers():
    result = add_two_numbers(10, 5)
    assert result == 20
def test_subtract_two_numbers():
    result = subtract_two_numbers(10, 5)
    assert result == 5
def test_multiply_two_numbers():
    result = multiply_two_numbers(10, 5)
    assert result == 50
def test_divide_two_numbers():
    result = divide_two_numbers(10, 5)
    assert result == 89