try:
    numerator = float(input("Enter numerator: "))
    denominator = float(input("Enter denominator: "))

    result = numerator / denominator

    print("Result =", result)

except ZeroDivisionError:
    print("Error: Denominator cannot be 0")