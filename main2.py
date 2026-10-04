import json
import os

FILE_NAME = "students.json"


# Load students from file
def load_students():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


# Save students to file
def save_students(students):
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


# Calculate average marks
def calculate_average(marks):
    return sum(marks) / len(marks)


# Add a student
def add_student(students):
    print("\n--- Add Student ---")

    name = input("Student Name: ")
    age = int(input("Age: "))
    department = input("Department: ")

    marks_input = input("Marks (comma separated): ")
    marks = [float(mark.strip()) for mark in marks_input.split(",")]

    attendance = float(input("Attendance (%): "))

    student = {
        "name": name,
        "age": age,
        "department": department,
        "marks": marks,
        "attendance": attendance
    }

    students.append(student)
    save_students(students)

    print("Student added successfully.")


# Display all students
def view_students(students):
    print("\n--- Student Records ---")

    if not students:
        print("No student records found.")
        return

    for student in students:
        average = calculate_average(student["marks"])

        print("\nName       :", student["name"])
        print("Age        :", student["age"])
        print("Department :", student["department"])
        print("Marks      :", student["marks"])
        print("Average    :", round(average, 2), "%")
        print("Attendance :", student["attendance"], "%")


# Search student
def search_student(students):
    name = input("\nSearch student: ")

    for student in students:
        if student["name"].lower() == name.lower():
            average = calculate_average(student["marks"])

            print("\nStudent Found")
            print("-------------")
            print("Name       :", student["name"])
            print("Age        :", student["age"])
            print("Department :", student["department"])
            print("Average    :", round(average, 2), "%")
            print("Attendance :", student["attendance"], "%")

            return

    print("Student not found.")


# Update student
def update_student(students):
    name = input("\nEnter student name to update: ")

    for student in students:
        if student["name"].lower() == name.lower():

            print("\nStudent Found")

            student["age"] = int(input("New Age: "))
            student["department"] = input("New Department: ")

            marks_input = input("New Marks (comma separated): ")
            student["marks"] = [
                float(mark.strip())
                for mark in marks_input.split(",")
            ]

            student["attendance"] = float(
                input("New Attendance (%): ")
            )

            save_students(students)

            print("Student updated successfully.")
            return

    print("Student not found.")


# Delete student
def delete_student(students):
    name = input("\nEnter student name to delete: ")

    for student in students:
        if student["name"].lower() == name.lower():
            students.remove(student)
            save_students(students)

            print("Student deleted successfully.")
            return

    print("Student not found.")


# Performance report
def performance_report(students):
    if not students:
        print("\nNo student records found.")
        return

    print("\n========== PERFORMANCE REPORT ==========")

    for student in students:
        average = calculate_average(student["marks"])

        if average >= 75:
            performance = "Excellent"
        elif average >= 60:
            performance = "Good"
        elif average >= 50:
            performance = "Average"
        else:
            performance = "Needs Improvement"

        if average >= 40:
            result = "PASS"
        else:
            result = "FAIL"

        print("\nName       :", student["name"])
        print("Average    :", round(average, 2), "%")
        print("Attendance :", student["attendance"], "%")
        print("Performance:", performance)
        print("Result     :", result)

        if student["attendance"] < 75:
            print("Warning    : Attendance below 75%")


# Main program
def main():
    students = load_students()

    while True:
        print("\n===================================")
        print(" STUDENT RECORD MANAGEMENT SYSTEM")
        print("===================================")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Performance Report")
        print("7. Save Records")
        print("8. Exit")
        print("===================================")

        choice = input("Choose an option: ")

        if choice == "1":
            add_student(students)

        elif choice == "2":
            view_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            update_student(students)

        elif choice == "5":
            delete_student(students)

        elif choice == "6":
            performance_report(students)

        elif choice == "7":
            save_students(students)
            print("Records saved successfully.")

        elif choice == "8":
            save_students(students)
            print("Records saved. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


main()
