numlist=[]
primelist=[]
nonprime=[]
def is_prime(num):
  if num<2:
    return False
  for i in range(2,num):
    if num%i==0:
      return False
  return True

n=int(input("Enter the number of element: "))
for i in range(n):
  num=int(input("Ente the number: "))
  numlist.append(num)
for num in numlist:
  if is_prime(num):
    primelist.append(num)
  else:
    nonprime.append(num)

print("The Prime number is: ",primelist)
print("The Non-prime number is: ",nonprime)
print("count the number of prime number is: ",len(primelist))
print("Count the number of non-prime number is: ",len(nonprime))
