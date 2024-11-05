class Student:
 def Getvalue(self):
    print("It is from base class!")
    self.rollno =input("Enter Rollno : ")
    self.name = input("Enter Name : ")
    self.department =input("Enter department : ")

 def Printvalue(self):
    print("\n\t MULTILEVEL INHERITANCE!\n")
    print("It is from base class!")
    print("Roll no : ", self.rollno)
    print("Name : ", self.name)
    print("Department : ", self.department)

###derived class
class Master(Student):
 def Getvalue(self):
    Student.Getvalue(self)
    print("It is from derived class!")
    self.sports =input("Enter Sports activity : ")
    self.ocourse = input("Enter online course name : ")

 def Printvalue(self):
    Student.Printvalue(self)
    print("It is from derived class!")
    print("Sports : ", self.sports)
    print("Online Course : ", self.ocourse)

class Extra_curricular(Master):
 def Getvalue(self):

    Master.Getvalue(self)
    print("It is from second level derived class!")
    self.hobby =input("Enter Hobby : ")

 def Printvalue(self):
    Master.Printvalue(self)
    print("It is from second level derived class!")
    print("Hobby : ", self.hobby)

##x=person()
##x.getinput()
##x.dispvalue()

##y=Master()
##y.Getvalue()
##y.Printvalue()

z=Extra_curricular()
z.Getvalue()
z.Printvalue()
