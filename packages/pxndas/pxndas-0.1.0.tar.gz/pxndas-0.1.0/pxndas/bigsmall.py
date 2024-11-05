num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
num3 = int(input("Enter the third number: "))

# Find the biggest number
if num1 >= num2 and num1 >= num3:
    biggest = num1
elif num2 >= num1 and num2 >= num3:
    biggest = num2
else:
    biggest = num3

# Find the smallest number
if num1 <= num2 and num1 <= num3:
    smallest = num1
elif num2 <= num1 and num2 <= num3:
    smallest = num2
else:
    smallest = num3

# Print the results
print("Biggest number:", biggest)
print("Smallest number:", smallest)
