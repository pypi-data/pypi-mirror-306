class Student:
  def __init__(self, rollno=None, name=None, dept=None):
    self.rollno =rollno
    self.name = name
    self.dept = dept


  def getvalue(self):
    self.rollno= int(input("Enter Rollno : "))
    self.name=input("Enter name : ")
    self.dept = input("Enter department : ")

  def printvalue(self):
    print(self.rollno)
    print(self.name)
    print(self.dept)

class master(Student):
  def __init__(self, rollno=None, name=None, dept=None, sports=None, ocourse=None):
    super().__init__(rollno,name,dept)
    self.sports = sports
    self.ocourse = ocourse


  def getvalue(self):
    super().getvalue()
    self.sports=input("Enter couse : ")
    self.ocourse = input("Enter online course : ")

  def printvalue(self):
    super().printvalue()
    print(self.sports)
    print(self.ocourse)

if __name__=="__main__":
  m=master()
  m.getvalue()
  m.printvalue()

