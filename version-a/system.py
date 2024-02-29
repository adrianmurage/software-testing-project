from user import Admin, Lecturer, Student, User
from course import Course

import json
import getpass


class System:
    """
    Represents a Course Registration System.

    Attributes:
    - users: A dictionary containing the users of the system, where the keys are usernames and the values are User objects.
    - courses: A list of Course objects representing the available courses in the system.

    Methods:
    - load_users: Loads the users from a JSON file and returns a dictionary of User objects.
    - load_courses: Loads the courses from a JSON file and returns a list of Course objects.
    - authenticate: Authenticates a user based on their username and password.
    - run: Starts the Course Registration System and prompts the user to log in.
    - admin_interface: Displays the admin interface and handles admin-specific actions.
    - lecturer_interface: Displays the lecturer interface and handles lecturer-specific actions.
    - student_interface: Displays the student interface and handles student-specific actions.
    """

    def __init__(self):
        self.users = self.load_users()
        self.courses = self.load_courses()

    def load_users(self):
        # Load users from the 'users.json' file
        with open('users.json') as f:
            users_json = json.load(f)

        # Create User objects based on the role specified in the JSON file
        users = {
            username: (
                User if role == 'User' else
                Admin if role == 'Admin' else
                Lecturer if role == 'Lecturer' else
                Student
            )(username, password)
            for username, password, role in users_json
        }

        return users

    def load_courses(self):
        # Load courses from the 'courses.json' file
        with open('courses.json') as f:
            courses_json = json.load(f)

        # Create Course objects based on the data in the JSON file
        courses = [
            Course(name, is_open, prerequisite, capacity)
            for name, is_open, prerequisite, capacity in courses_json
        ]

        return courses

    def save_courses(self):
        # Convert the courses to a JSON-serializable format
        courses_json = [
            (course.name, course.is_open, course.prerequisite, course.capacity)
            for course in self.courses
        ]
        # Save the courses to the 'courses.json' file
        with open('courses.json', 'w') as f:
            json.dump(courses_json, f)

    def load_schedules(self):
        try:
            with open('schedules.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_schedules(self):
        with open('schedules.json', 'w') as f:
            json.dump(self.schedules, f)

    def register_for_class(self, username, course):
        if username not in self.schedules:
            self.schedules[username] = []
        self.schedules[username].append(course.name)
        self.save_schedules()

    def authenticate(self, username, password):
        return username in self.users and self.users[username].password == password

    def run(self):
        while True:
            print("\nWelcome to the Course Registration System")
            print("Please log in or type 'exit' to quit")
            username = input("Username: ")
            if username.lower() == 'exit':
                self.save_courses()     
                return
            password = getpass.getpass()
            if password.lower() == 'exit':
                self.save_courses()     
                return
            if self.authenticate(username, password):
                print("Login successful")
                user = self.users[username]
                if isinstance(user, Admin):
                    self.admin_interface(user)
                elif isinstance(user, Lecturer):
                    self.lecturer_interface(user)
                elif isinstance(user, Student):
                    self.student_interface(user)
            else:
                print("Login failed")
        

    def admin_interface(self, user):
        user = Admin(user.username, user.password)
        while True:
            print("\n1. Add course")
            print("2. Update course")
            print("3. Delete course")
            print("4. View courses")
            print("5. Logout")
            print("--------------------")
            choice = input("Choose an option or type 'exit' to quit: ")
            if choice.lower() == 'exit':
                self.save_courses()     
                return

            if choice == '1':
                name = input("Enter course name: ")
                is_open = input("Is the course open? (yes/no): ") == 'yes'
                prerequisite = input(
                    "Enter the prerequisite course (or 'none' if there is none): ")
                if prerequisite.lower() == 'none':
                    prerequisite = None
                capacity = int(input("Enter the capacity of the course: "))
                self.courses = user.add_course(
                    Course(name, is_open, prerequisite, capacity), self.courses)
            elif choice == '2':
                name = input("Enter course name: ")
                new_name = input("Enter new course name: ")
                is_open = input("Is the course open? (yes/no): ") == 'yes'
                prerequisite = input(
                    "Enter the prerequisite course (or 'none' if there is none): ")
                if prerequisite.lower() == 'none':
                    prerequisite = None
                capacity = int(
                    input("Enter the new capacity of the course: "))
                self.courses = user.update_course(name, Course(
                    new_name, is_open, prerequisite, capacity), self.courses)
            elif choice == '3':
                name = input("Enter course name: ")
                self.courses = user.delete_course(name, self.courses)
            elif choice == '4':
                user.view_courses(self.courses)
            elif choice == '5':
                break
        self.save_courses()

    def lecturer_interface(self, user):
        user = Lecturer(user.username, user.password)
        while True:
            print("\n1. Select course")
            print("2. Select room")
            print("3. View courses")
            print("4. Logout")
            print("--------------------")
            choice = input("Choose an option or type 'exit' to quit: ")
            if choice.lower() == 'exit':
                return

            if choice == '1':
                name = input("Enter course name: ")
                for course in self.courses:
                    if course.name == name:
                        user.select_course(course)
                        break
            elif choice == '2':
                room = input("Enter room: ")
                user.select_room(room)
            elif choice == '3':
                user.view_courses(self.courses)
            elif choice == '4':
                break

    def student_interface(self, user):
        user = Student(user.username, user.password)
        while True:
            print("\n1. Register for class")
            print("2. View schedule")
            print("3. Add class")
            print("4. Drop class")
            print("5. View classes")
            print("6. Logout")
            print("--------------------")
            choice = input("Choose an option or type 'exit' to quit: ")
            if choice.lower() == 'exit':
                return

            if choice == '1':
                name = input("Enter course name: ")
                for course in self.courses:
                    if course.name == name:
                        user.register_for_class(course, self)
                        break
            elif choice == '2':
                user.view_schedule()
            elif choice == '3':
                name = input("Enter course name: ")
                for course in self.courses:
                    if course.name == name:
                        user.add_class(course)
                        break
            elif choice == '4':
                name = input("Enter course name: ")
                user.drop_class(name)
            elif choice == '5':
                user.view_classes(self.courses)
            elif choice == '6':
                break
