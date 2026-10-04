import json
import os
import requests


# ============================================================
# Student Class
# ============================================================

class Student:

    def __init__(
        self,
        student_id,
        name,
        age,
        department,
        marks,
        attendance,
        status="Active"
    ):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.department = department
        self.marks = marks
        self.attendance = attendance
        self.status = status

    def calculate_average(self):

        if not self.marks:
            return 0

        return sum(self.marks) / len(self.marks)

    def get_performance(self):

        average = self.calculate_average()

        if average >= 75:
            return "Excellent"

        elif average >= 60:
            return "Good"

        elif average >= 50:
            return "Average"

        else:
            return "Needs Improvement"

    def get_result(self):

        if self.calculate_average() >= 40:
            return "PASS"

        return "FAIL"

    def update(
        self,
        name=None,
        age=None,
        department=None,
        marks=None,
        attendance=None,
        status=None
    ):

        if name:
            self.name = name

        if age is not None:
            self.age = age

        if department:
            self.department = department

        if marks is not None:
            self.marks = marks

        if attendance is not None:
            self.attendance = attendance

        if status:
            self.status = status


# ============================================================
# StudentManager Class
# ============================================================

class StudentManager:

    def __init__(self):
        self.students = {}

    def add_student(self, student):

        if student.student_id in self.students:
            print("Error: Student ID already exists.")
            return False

        self.students[student.student_id] = student

        print("Student added successfully.")
        return True

    def get_student(self, student_id):

        return self.students.get(student_id)

    def update_student(self, student_id, **kwargs):

        student = self.get_student(student_id)

        if student is None:
            print("Error: Student not found.")
            return False

        student.update(**kwargs)

        print("Student updated successfully.")
        return True

    def delete_student(self, student_id):

        if student_id not in self.students:
            print("Error: Student not found.")
            return False

        del self.students[student_id]

        print("Student deleted successfully.")
        return True

    def get_all_students(self):

        return list(self.students.values())

    def display_all(self):

        if not self.students:
            print("No student records found.")
            return

        print("\n========== STUDENTS ==========")

        for student in self.students.values():

            print("\nID:", student.student_id)
            print("Name:", student.name)
            print("Department:", student.department)
            print("Average:",
                  round(student.calculate_average(), 2))
            print("Attendance:",
                  student.attendance)


# ============================================================
# ReportGenerator Class
# ============================================================

class ReportGenerator:

    @staticmethod
    def student_report(student):

        print("\nStudent Report")
        print("---------------")

        print(
            f"{student.student_id} | "
            f"{student.name} | "
            f"{student.department}"
        )

        print(
            f"Average: "
            f"{student.calculate_average():.1f}%"
        )

        print(
            f"Attendance: "
            f"{student.attendance}%"
        )

        print(
            f"Performance: "
            f"{student.get_performance()}"
        )

        print(
            f"Status: "
            f"{student.status}"
        )

    @staticmethod
    def class_report(manager):

        students = manager.get_all_students()

        if not students:
            print("No students available.")
            return

        total = len(students)

        class_average = sum(
            student.calculate_average()
            for student in students
        ) / total

        top_student = max(
            students,
            key=lambda student:
            student.calculate_average()
        )

        print("\n========== CLASS REPORT ==========")

        print("Total Students:", total)

        print(
            "Average Class Mark:",
            round(class_average, 2)
        )

        print("\nTop Performer:")

        print(
            f"{top_student.name} - "
            f"Average: "
            f"{top_student.calculate_average():.1f}%"
        )

        print("\nResults:")

        for student in students:

            print(
                f"{student.name} - "
                f"{student.get_result()}"
            )


# ============================================================
# FileManager Class
# ============================================================

class FileManager:

    FILE_NAME = "students.json"

    @staticmethod
    def save(manager):

        data = []

        for student in manager.get_all_students():

            data.append({
                "student_id": student.student_id,
                "name": student.name,
                "age": student.age,
                "department": student.department,
                "marks": student.marks,
                "attendance": student.attendance,
                "status": student.status
            })

        try:

            with open(
                FileManager.FILE_NAME,
                "w"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

            print("Records saved successfully.")

        except IOError:

            print("Error: Could not save records.")

    @staticmethod
    def load(manager):

        if not os.path.exists(
            FileManager.FILE_NAME
        ):
            return

        try:

            with open(
                FileManager.FILE_NAME,
                "r"
            ) as file:

                data = json.load(file)

            for item in data:

                student = Student(
                    item["student_id"],
                    item["name"],
                    item["age"],
                    item["department"],
                    item["marks"],
                    item["attendance"],
                    item["status"]
                )

                manager.students[
                    student.student_id
                ] = student

            print("Records loaded successfully.")

        except (
            IOError,
            json.JSONDecodeError,
            KeyError
        ):

            print("Error: Invalid student data file.")


# ============================================================
# CountryAPI Class
# ============================================================

class CountryAPI:

    BASE_URL = "https://restcountries.com/v3.1/name/"

    @staticmethod
    def get_country(country_name):

        if not country_name.strip():

            print("Error: Country name cannot be empty.")
            return

        url = (
            CountryAPI.BASE_URL
            + country_name.strip()
        )

        try:

            response = requests.get(
                url,
                timeout=10
            )

            # No matching country
            if response.status_code == 404:

                print(
                    "No matching country found."
                )

                return

            # Other API errors
            if response.status_code != 200:

                print(
                    "API unavailable. "
                    f"Status code: "
                    f"{response.status_code}"
                )

                return

            try:

                data = response.json()

            except ValueError:

                print(
                    "Error: Invalid API response."
                )

                return

            if not isinstance(data, list) or not data:

                print(
                    "Error: Invalid country data."
                )

                return

            country = data[0]

            # Check required fields
            name = country.get(
                "name", {}
            ).get(
                "common",
                "Unknown"
            )

            capital_list = country.get(
                "capital",
                []
            )

            capital = (
                capital_list[0]
                if capital_list
                else "N/A"
            )

            population = country.get(
                "population",
                0
            )

            region = country.get(
                "region",
                "N/A"
            )

            currencies = country.get(
                "currencies",
                {}
            )

            if currencies:

                currency_code = list(
                    currencies.keys()
                )[0]

            else:

                currency_code = "N/A"

            # Display useful information only
            print("\nCountry Information")
            print("-------------------")

            print("Name       :", name)
            print("Capital    :", capital)
            print("Population :", format_population(
                population
            ))
            print("Region     :", region)
            print("Currency   :", currency_code)

        except requests.exceptions.Timeout:

            print(
                "Network error: "
                "The request timed out."
            )

        except requests.exceptions.ConnectionError:

            print(
                "Network error: "
                "Could not connect to the API."
            )

        except requests.exceptions.RequestException:

            print(
                "Network error: "
                "Unable to contact the API."
            )

        except Exception:

            print(
                "Unexpected error while "
                "processing country information."
            )


# ============================================================
# Helper Function
# ============================================================

def format_population(population):

    if population >= 1_000_000_000:

        return (
            f"{population / 1_000_000_000:.1f}B"
        )

    elif population >= 1_000_000:

        return (
            f"{population / 1_000_000:.1f}M"
        )

    elif population >= 1_000:

        return (
            f"{population / 1_000:.1f}K"
        )

    return str(population)


# ============================================================
# Student Creation
# ============================================================

def create_student(manager):

    print("\n--- Add Student ---")

    student_id = input(
        "Student ID: "
    ).strip()

    if manager.get_student(student_id):

        print(
            "Error: Student ID already exists."
        )

        return

    name = input(
        "Name: "
    ).strip()

    try:

        age = int(
            input("Age: ")
        )

    except ValueError:

        print("Invalid age.")
        return

    department = input(
        "Department: "
    ).strip()

    try:

        marks_input = input(
            "Marks (comma separated): "
        )

        marks = [
            float(mark.strip())
            for mark in marks_input.split(",")
        ]

    except ValueError:

        print("Invalid marks.")
        return

    try:

        attendance = float(
            input("Attendance (%): ")
        )

    except ValueError:

        print("Invalid attendance.")
        return

    if any(
        mark < 0 or mark > 100
        for mark in marks
    ):

        print(
            "Marks must be between "
            "0 and 100."
        )

        return

    if attendance < 0 or attendance > 100:

        print(
            "Attendance must be between "
            "0 and 100."
        )

        return

    student = Student(
        student_id,
        name,
        age,
        department,
        marks,
        attendance
    )

    manager.add_student(student)


# ============================================================
# Search Student
# ============================================================

def search_student(manager):

    keyword = input(
        "\nSearch by ID, name, or department: "
    ).strip()

    found = False

    for student in manager.get_all_students():

        if (
            keyword.lower()
            in student.name.lower()
            or keyword.lower()
            in student.student_id.lower()
            or keyword.lower()
            in student.department.lower()
        ):

            ReportGenerator.student_report(
                student
            )

            found = True

    if not found:

        print(
            "No matching student found."
        )


# ============================================================
# Main Program
# ============================================================

def main():

    manager = StudentManager()

    # Load saved student records
    FileManager.load(manager)

    while True:

        print("\n======================================")
        print(" STUDENT RECORD MANAGEMENT SYSTEM")
        print("======================================")

        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Student Performance Report")
        print("7. Class Report")
        print("8. Save Records")
        print("9. Country Information")
        print("10. Exit")

        print("======================================")

        choice = input(
            "Choose an option: "
        ).strip()

        # Add student
        if choice == "1":

            create_student(manager)

        # View students
        elif choice == "2":

            manager.display_all()

        # Search student
        elif choice == "3":

            search_student(manager)

        # Update student
        elif choice == "4":

            student_id = input(
                "Enter Student ID: "
            ).strip()

            student = manager.get_student(
                student_id
            )

            if student is None:

                print("Student not found.")

            else:

                name = input(
                    f"New Name "
                    f"[{student.name}]: "
                ).strip()

                department = input(
                    f"New Department "
                    f"[{student.department}]: "
                ).strip()

                if name:

                    student.name = name

                if department:

                    student.department = department

                FileManager.save(manager)

                print(
                    "Student updated successfully."
                )

        # Delete student
        elif choice == "5":

            student_id = input(
                "Enter Student ID: "
            ).strip()

            manager.delete_student(
                student_id
            )

        # Student performance
        elif choice == "6":

            student_id = input(
                "Enter Student ID: "
            ).strip()

            student = manager.get_student(
                student_id
            )

            if student:

                ReportGenerator.student_report(
                    student
                )

            else:

                print(
                    "Student not found."
                )

        # Class report
        elif choice == "7":

            ReportGenerator.class_report(
                manager
            )

        # Save records
        elif choice == "8":

            FileManager.save(manager)

        # Country API
        elif choice == "9":

            country = input(
                "\nEnter country: "
            ).strip()

            CountryAPI.get_country(
                country
            )

        # Exit
        elif choice == "10":

            FileManager.save(manager)

            print(
                "Records saved."
            )

            print(
                "Thank you. Goodbye!"
            )

            break

        else:

            print(
                "Invalid option. "
                "Please choose a valid option."
            )


# ============================================================
# Program Start
# ============================================================

if __name__ == "__main__":
    main()
