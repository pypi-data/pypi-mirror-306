import numpy as np 
m=int(input("Enter the no.of Rows:"))
n=int(input("Enter the no.of Columns:"))
tot_ele = m*n
print("Enter the Elements of 'A' matrix")
A=np.zeros(tot_ele)
A=np.reshape(A,(m,n))
for i in range(m):
  for j in range(n):
    A[i,j]=int(input())
print(A)
print("Enter the Elements of 'B' matrix")
B=np.zeros(tot_ele)
B=np.reshape(B,(m,n))
for i in range(m):
  for j in range(n):
    B[i,j]=int(input())
print(B)
# adding A and B
C=np.zeros(tot_ele)
C=np.reshape(C,(m,n))
for i in range(m):
  for j in range(n):
    C[i,j]= A[i,j]+B[i,j]
print("Result of Matrix Addition")
print(C)
