def calculator():
  while True:
    print("\n Select operation:")
    print("1. Additon")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulus")
    print("6. Exponentiation")

    choice=input("Enter Choice(1/2/3/4/5/6):")

    num1=float(input("Enter first number:"))
    num2=float(input("Enter second number:"))

    if choice == '1':
      print(f"Result: {num1+num2}")
    elif choice=='2':
      print(f"Result: {num1-num2}")
    elif choice=='3':
      print(f"Result: {num1*num2}")
    elif choice=='4':
      print(f"Result: {'Error:Divison by zero'if num2==0 else num1/num2}")
    elif choice=='5':
      print(f"Result: {num1%num2}")
    elif choice=='6':
      print(f"Result: {num1**num2}")
    else:
       print("Invalid input")

    if input("Press 'Yes' to continue or any other key to exit:")!='Yes':
      break

calculator()
