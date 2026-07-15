password = input("Enter password: ")

length = len(password)

if length >= 10 and length <= 16:
    print("Valid Password")
else:
    print("Invalid Password")