import json
import hashlib


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'user_type': self.__class__.__name__
        }

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()


class Student(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.courses = []

    def register_for_course(self, course):
        course.register_student(self)
        self.courses.append(course)

    def study(self):
        print(f'{self.username} is studying.')


class Lecturer(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.courses = []

    def assign_course(self, course):
        self.courses.append(course)

    def teach(self):
        print(f'{self.username} is teaching.')


class Course:
    def __init__(self, course_name):
        self.course_name = course_name
        self.students = []

    def register_student(self, student):
        if isinstance(student, Student):
            self.students.append(student)
            print(
                f'Student {student.username} has been registered for {self.course_name}.')
        else:
            print('Only students can register for courses.')

    def to_dict(self):
        return {
            'course_name': self.course_name,
            'students': [student.username for student in self.students]
        }


class LoginApplication:
    def __init__(self):
        self.users = []
        self.courses = []

    def register_user(self, username, password, user_type):
        if any(user.username == username for user in self.users):
            print('User already exists')
            return
        if user_type.lower() == 'student':
            user = Student(username, password)
        elif user_type.lower() == 'lecturer':
            user = Lecturer(username, password)
        else:
            print('Invalid user type')
            return
        self.users.append(user)

    def login(self, username, password):
        hashed_password = User.hash_password(password)
        for user in self.users:
            if user.username == username and user.password == hashed_password:
                return user
        return None

    def save_users_to_file(self, filename):
        user_data = [user.to_dict() for user in self.users]
        with open(filename, 'w') as file:
            json.dump(user_data, file)

    def load_users_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                user_data = json.load(file)
                for data in user_data:
                    if 'username' in data and 'password' in data and 'user_type' in data:
                        if data['user_type'] == 'Student':
                            self.users.append(
                                Student(data['username'], data['password']))
                        elif data['user_type'] == 'Lecturer':
                            self.users.append(
                                Lecturer(data['username'], data['password']))
                    else:
                        print('Invalid user data, skipping.')
        except FileNotFoundError:
            print(f"{filename} not found. Starting with no users.")

    def save_courses_to_file(self, filename):
        course_data = [course.to_dict() for course in self.courses]
        with open(filename, 'w') as file:
            json.dump(course_data, file)

    def load_courses_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                course_data = json.load(file)
                for data in course_data:
                    course = Course(data['course_name'])
                    for username in data['students']:
                        for user in self.users:
                            if user.username == username and isinstance(user, Student):
                                course.students.append(user)
                                user.courses.append(course)
                    self.courses.append(course)
        except FileNotFoundError:
            print(f"{filename} not found. Starting with no courses.")


def main():
    app = LoginApplication()
    app.load_users_from_file('users.json')
    app.load_courses_from_file('courses.json')

    courses = [Course('Math'), Course('English'), Course('Science')]

    while True:
        command = input('Enter a command (register, login, exit): ')

        if command == 'register':
            username = input('Enter username: ')
            password = input('Enter password: ')
            user_type = input('Enter user type (student/lecturer): ')
            app.register_user(username, password, user_type)
            app.save_users_to_file('users.json')

        elif command == 'login':
            username = input('Enter username: ')
            password = input('Enter password: ')
            user = app.login(username, password)
            if user:
                print('Login successful')
                if isinstance(user, Student):
                    while True:
                        command = input(
                            'Enter a command (register for course, study, logout): ')
                        if command == 'register for course':
                            for i, course in enumerate(app.courses, 1):
                                print(f'{i}. {course.course_name}')
                            course_number = int(input('Enter course number: '))
                            if 1 <= course_number <= len(app.courses):
                                user.register_for_course(
                                    app.courses[course_number - 1])
                            else:
                                print('Invalid course number')
                        elif command == 'study':
                            user.study()
                        elif command == 'logout':
                            break
                        else:
                            print('Invalid command')
                elif isinstance(user, Lecturer):
                    while True:
                        command = input(
                            'Enter a command (assign course, teach, logout): ')
                        if command == 'assign course':
                            for i, course in enumerate(app.courses, 1):
                                print(f'{i}. {course.course_name}')
                            course_number = int(input('Enter course number: '))
                            if 1 <= course_number <= len(app.courses):
                                user.assign_course(
                                    app.courses[course_number - 1])
                            else:
                                print('Invalid course number')
                        elif command == 'teach':
                            user.teach()
                        elif command == 'logout':
                            break
                        else:
                            print('Invalid command')
            else:
                print('Login failed')

        elif command == 'exit':
            confirm = input('Are you sure you want to exit? (yes/no): ')
            if confirm.lower() == 'yes':
                break

        else:
            print('Invalid command')

    app.save_users_to_file('users.json')
    app.save_courses_to_file('courses.json')


if __name__ == '__main__':
    main()
