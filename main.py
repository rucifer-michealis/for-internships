students = [
    {
        "name": "Dass",
        "age": 20,
        "department": "CSE",
        "marks": [78, 85, 72],
        "attendance": 91
    },
    {
        "name": "Chandra",
        "age": 21,
        "department": "CSE",
        "marks": [65, 71, 68],
        "attendance": 84
    },
    {
        "name": "Parvathi",
        "age": 20,
        "department": "ECE",
        "marks": [45, 52, 48],
        "attendance": 72
    }
]

PASS_MARK = 40


def average_mark(student):
    return sum(student["marks"]) / len(student["marks"])


def display_students(students):
    for student in students:
        print(
            f'{student["name"]} - {student["department"]} - '
            f'Marks: {student["marks"]} - Attendance: {student["attendance"]}%'
        )


def result(student):
    return "PASS" if average_mark(student) >= PASS_MARK else "FAIL"


def top_performer(students):
    return max(students, key=average_mark)


def filter_by_attendance(students, limit):
    return [s for s in students if s["attendance"] < limit]


def filter_by_average_mark(students, minimum):
    return [s for s in students if average_mark(s) >= minimum]


def class_summary(students):
    total = len(students)
    class_average = sum(average_mark(s) for s in students) / total
    top = top_performer(students)

    print("\nClass Summary")
    print("-------------")
    print(f"Total Students: {total}")
    print(f"Average Class Mark: {class_average:.1f}")

    print("\nTop Performer:")
    print(f"{top['name']} - Average: {average_mark(top):.1f}%")

    print("\nAttendance Below 75%:")
    for student in filter_by_attendance(students, 75):
        print(f"{student['name']} - {student['attendance']}%")

    print("\nResult:")
    for student in students:
        print(f"{student['name']} - {result(student)}")


print("All Students")
print("------------")
display_students(students)

class_summary(students)