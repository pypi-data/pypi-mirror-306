print("\t EXCEPTION HANDLING \n")
def get_marks(course_number):
    while True:
        try:
            internal = float(input(f"Enter the internal marks for course {course_number}: "))
            if internal < 0 :
                raise ValueError("Marks should be positive or zero.")

            external = float(input(f"Enter the external marks for course {course_number}: ")) # Moved external input inside the loop
            if external < 0:
                raise ValueError("Marks should be positive or zero.")

            return internal, external # Return both internal and external marks
        except ValueError as e:
            print(e)
            print("Please enter valid marks.")

def calculate_grade(average):
    if average >= 90:
        return "O"
    elif average >= 80:
        return "A+"
    elif average >= 70:
        return "A"
    elif average >= 60:
        return "B+"
    elif average >= 50:
        return "B"
    else:
        return "Fail"

def main():
    marks_list = [] # Initialize marks_list
    total_marks = 0
    for i in range(1, 6):
        internal, external = get_marks(i)
        marks_list.append((internal, external)) # Append marks to marks_list
        if internal >= 13 and external >= 38 and (internal + external) >= 50:
            total_marks += (internal + external)
        else:
            print(f"Course {i} failed. Marks: Internal={internal}, External={external}")
    print("\n\t MARK FOR ALL COURSES")
    for i ,(internal,external)in enumerate(marks_list, 1):
        print(f"Course {i}: Internal={internal}, External={external}")
    average = total_marks / 5

    print(f"Total marks: {total_marks}")
    print(f"Average marks: {average:.2f}")

    grade = calculate_grade(average)
    print(f"Grade: {grade}")

if __name__ == "__main__":
    main()
