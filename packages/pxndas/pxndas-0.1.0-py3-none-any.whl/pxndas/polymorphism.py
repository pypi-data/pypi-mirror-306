class mylist:

 def getinput(self):
    print("\t POLYMORPHISM \n")
    list1=[]
    print("It is from List class")
    N=int(input("Enter the number of elements:"))
    for i in range(N):
        list=int(input("Enter the value:"))
        list1.append(list)
    self.lt=list1    
 def additem(self):
    msum=0
    for i in self.lt:
         msum=msum+i
    print("Sum of List elements :",msum)

class mytuple:
 def getinput(self):
    tuple1=[] 
    print("It is from Tuple class")
    M=int(input("Enter the number of elements:"))
    for i in range(M):
        tup=int(input("Enter the value:"))
        tuple1.append(tup)
    t1=tuple(tuple1)    
    self.tp=t1 
 def additem(self):
    msum=0
    for i in self.tp:
        msum=msum+i
    print("Sum of Tuple elements :",msum)

L1 = mylist()
T1= mytuple()

for i in (L1,T1):
 i.getinput()

for i in (L1,T1):
 i.additem()
