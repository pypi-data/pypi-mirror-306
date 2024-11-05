mylist=[]
N=int(input("Enter the number of element:"))

for i in range(N):
    num=int(input("Enter the number:"))
    mylist.append(num)

ev_li=[]
od_li=[]

for i in mylist:
    if (i%2==0):
       ev_li.append(i)
    else:
       od_li.append(i)

print("Even list:",ev_li)
print("Odd list:",od_li)

    
