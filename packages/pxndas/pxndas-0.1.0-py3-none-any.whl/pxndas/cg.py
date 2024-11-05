import tkinter as tk
master = tk.Tk()

master.title("CGPA Calculation")

master.geometry("1000x600")

master.configure(bg='white')

frame1 = tk.Frame(master, width=1000, height=150,bg='white')
frame1.pack(padx=20,pady=20)
tk.Label(frame1, text="Manonmaniam Sundaranar University",font=("Times New Roman",20, "bold"),bg='white').grid(row=1,column=7)
tk.Label(frame1, text="Reaccredited with 'A' Grade (CGPA 3.13 Out of 4.0) by NAAC (3rdCycle)",font=("Times New Roman", 10),bg='white').grid(row=2,column=7)
tk.Label(frame1, text="Tirunelveli - 627012, Tamil Nadu, India",font=("Times New Romsn",13),bg='white').grid(row=3,column=7)

##image=PhotoImage(file="logo.png") image_label =
##tk.Label(master,width=300,height=300, image=image).grid(row=2,column=5)
##image_label.pack()

frame2 = tk.Frame(master, width=1000, height=150,bg='white')
##frame3 = tk.Frame(master, width=1000, height=30,bg='white')
frame2.pack()
##frame3.pack()

prog = tk.Entry(frame2)
name = tk.Entry(frame2)
regNo = tk.Entry(frame2)
s1 = tk.Entry(frame2,width=10)
s2 = tk.Entry(frame2,width=10)
s3 = tk.Entry(frame2,width=10)
s4 = tk.Entry(frame2,width=10)
s5 = tk.Entry(frame2,width=10)
s6 = tk.Entry(frame2,width=10)
s7 = tk.Entry(frame2,width=10)
s8 = tk.Entry(frame2,width=10)

tk.Label(frame2, text="Programme:",bg='white').grid(row=3, column=2)
prog.grid(row=3, column=3)
tk.Label(frame2, text="Name:",bg='white').grid(row=3, column=5)
name.grid(row=3, column=6)
tk.Label(frame2, text="Reg.No:",bg='white').grid(row=3, column=7)
regNo.grid(row=3, column=8)

## Print serial numbers
tk.Label(frame2, text="S.No",bg='white').grid(row=4,column=2,pady=20)
for i in range(8):
    tk.Label(frame2, text=i+1,bg='white').grid(row=i+5, column=2)

## Print subjects
subList = ["Discrete Mathematics","Linux and shell programming","Pythonprogramming","Data Engineerring","Soft Computing","Data Engineering Lab","PythonProgramming Lab","Skill Enhancement Course"]
tk.Label(frame2, text="Subject",bg='white').grid(row=4,column=3,pady=20)
for i in range(len(subList)):
           tk.Label(frame2, text=subList[i],bg='white').grid(row=i+5, column=3,sticky="w")

## Print subject credits
scredits = [4,4,4,4,4,2,2,1]
tk.Label(frame2, text="Sub Credit",bg='white').grid(row=4,column=5,pady=20)
for i in range(len(scredits)):
           tk.Label(frame2, text=scredits[i],bg='white').grid(row=i+5, column=5)

## grade inputs
entry = [s1,s2,s3,s4,s5,s6,s7,s8]
tk.Label(frame2, text="Grade",bg='white').grid(row=4,column=6,pady=20)
for i in range(len(entry)):
           entry[i].grid(row=i+5, column=6,padx=15)

tk.Label(frame2, text="Grade Point",bg='white').grid(row=4,column=7,pady=20)
tk.Label(frame2, text="Credit Obtained",bg='white').grid(row=4,column=8,pady=20,padx=10)

gradeDict = {"O": 10,"A+": 9,"A": 8,"B+": 7,"B": 6,"C": 5}

def calculate():
    clist = []
    c=0
    gc=0
    cgpa=0
    for widget in frame2.grid_slaves(row=19, column=8):
        widget.grid_forget()

    for i in range(len(entry)):
        val = entry[i].get().upper()
        clist.append(val.upper())
        if(val in gradeDict):
            credit = gradeDict[val]
            c+=scredits[i]
            gc+=credit*scredits[i]
            tk.Label(frame2, text=credit,bg='white').grid(row=i+5, column=7)
            tk.Label(frame2, text= credit*scredits[i],bg='white').grid(row=i+5, column=8)
        else:
             if(val == "RA"):
                 tk.Label(frame2, text="RA",bg='white').grid(row=i+5, column=7)
                 tk.Label(frame2, text=" RA ",bg='white').grid(row=i+5, column=8)
             elif(val == "AA"):
                 tk.Label(frame2, text="AA",bg='white').grid(row=i+5, column=7)
                 tk.Label(frame2, text=" AA ",bg='white').grid(row=i+5, column=8)
             else:
                 tk.Label(frame2, text=" - ",bg='white').grid(row=i+5, column=7)
                 tk.Label(frame2, text=" - ",bg='white').grid(row=i+5, column=8)

    if(gc!=0 and c!=0):
        if("RA" not in clist and "AA" not in clist):
            cgpa=gc/c
        else:
            cgpa = 0
##            tk.Label(master, text=" Cant calculate CGPA",bg='white',fg="black").place(x=615,y=475)

    tk.Label(frame2, text=gc,bg='white').grid(row=18,column=8,pady=20)
    tk.Label(frame2, text=" "+str(cgpa)+" ",bg='white').grid(row=19,column=8)

##def clear():

tk.Button(frame2, text =
"Calculate",width=10,bg='white',command=calculate).grid(row=18,column=6)
##tk.Button(frame2, text = "Clear",width=10,command=clear).grid(row=20,column=6)
tk.Label(frame2, text="Total",bg='white').grid(row=18,column=7,pady=20)
tk.Label(frame2, text="CGPA",bg='white').grid(row=19,column=7)
master.mainloop()
