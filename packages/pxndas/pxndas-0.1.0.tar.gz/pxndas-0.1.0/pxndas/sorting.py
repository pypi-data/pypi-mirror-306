n1=[]
n=int(input("Enter the number of elements:"))
for i in range(n):
    value=int(input("Enter value:"))
    n1.append(value)

print("Elements before sorting: ",n1)

for i in range(n):
    for j in range(i+1,n):
        if n1[i]>n1[j]:
            n1[i],n1[j]=n1[j],n1[i]
print("Element after sorting in ascending order: ",n1)
print("Element after sorting in descending order: ",n1[::-1])
            
