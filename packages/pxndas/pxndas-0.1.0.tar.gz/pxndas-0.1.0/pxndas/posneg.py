N = int(input("Enter the number of elements: "))
positive_numbers = ()
negative_numbers=()

for i in range(N):
    num = int(input(f"Enter a number{i+1}: "))
    if (num>=0):
        positive_numbers+=(num,)
    else:
        negative_numbers+=(num,)


print("Positive numbers:", positive_numbers)
print("Negative numbers:", negative_numbers)

