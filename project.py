class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Student(User):
    def __init__(self, username, password, gpa):
        super().__init__(username, password)
        self.gpa = gpa
        self.classes_taken = []

    def register_for_class(self, course):
        if course.is_open and course.prerequisites_met(self):
            self.classes_taken.append(course)
            print(f"Successfully registered for {course.name}")
        else:
            print("Unable to register for the class.")

    def check_financial_clearance(self):
        # Simulated financial clearance check
        return True


class Course:
    def __init__(self, name, is_open, prerequisites, required_gpa):
        self.name = name
        self.is_open = is_open
        self.prerequisites = prerequisites
        self.required_gpa = required_gpa

    def prerequisites_met(self, student):
        return all(prerequisite in student.classes_taken for prerequisite in self.prerequisites) \
               and student.gpa >= self.required_gpa


class Lecturer(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def book_room(self, course, room):
        print(f"Room {room} booked for {course.name}.")


class SchoolSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.lecturers = []

    def add_student(self, student):
        self.students.append(student)

    def add_course(self, course):
        self.courses.append(course)

    def add_lecturer(self, lecturer):
        self.lecturers.append(lecturer)

    def display_available_classes(self):
        print("Available Classes:")
        for course in self.courses:
            print(course.name)


# Example usage
school = SchoolSystem()

# Creating courses
math_course = Course("Mathematics", is_open=True, prerequisites=[], required_gpa=3.0)
physics_course = Course("Physics", is_open=True, prerequisites=["Mathematics"], required_gpa=3.5)
chemistry_course = Course("Chemistry", is_open=False, prerequisites=["Physics"], required_gpa=3.7)

# Adding courses to the system
school.add_course(math_course)
school.add_course(physics_course)
school.add_course(chemistry_course)

# Creating students
student1 = Student("alice", "password123", 3.8)
student2 = Student("bob", "password456", 3.3)

# Adding students to the system
school.add_student(student1)
school.add_student(student2)

# Student registration
student1.register_for_class(math_course)
student2.register_for_class(chemistry_course)

# Display available classes
school.display_available_classes()
