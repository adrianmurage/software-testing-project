import json


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def add_course(self, course, courses):
        courses.append(course)
        print("\n------------------------")
        print(f"| Course {course.name} added successfully! |")
        print("------------------------\n")
        return courses

    def update_course(self, course_name, new_course, courses):
        for i, course in enumerate(courses):
            if course.name == course_name:
                courses[i] = new_course
        print("\n------------------------")
        print(f"| Course {course_name} updated successfully! |")
        print("------------------------\n")
        return courses

    def delete_course(self, course_name, courses):
        courses = [
            course for course in courses if course.name != course_name]
        print("\n------------------------")
        print(f"| Course {course_name} deleted successfully! |")
        print("------------------------\n")
        return courses

    def view_courses(self, courses):
        print("------------------------")
        for course in courses:
            print("|", course.name, "|")
        print("------------------------")


class Lecturer(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.course = None
        self.room = None

    def select_course(self, course):
        self.course = course

    def select_room(self, room):
        self.room = room

    def view_courses(self, courses):
        for course in courses:
            print(course.name)


class Student(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    # def register_for_class(self, course, system):
    #     if len(system.schedules.get(self.username, [])) < 5 or self.gpa >= 3.0:
    #         if course.add_student(self):
    #             system.register_for_class(self.username, course)
    #         else:
    #             print(f"The course {course.name} is full.")
    #     else:
    #         print("Cannot register for more than 5 classes with GPA less than 3.0")

    def view_schedule(self, schedules):
        for student in schedules:
            if student['name'] == self.username:
                print("\n------------------------")
                print(f"Schedule for {self.username}:")
                print("Courses:", ', '.join(student['courses']))
                print("Completed Courses:", ', '.join(
                    student['completed_courses']))
                print("GPA:", student['gpa'])
                print("------------------------")
                return
        print(f"No schedule found for {self.username}")

    def add_class(self, course_name, schedules):
        for student in schedules:
            if student['name'] == self.username:
                if len(student['courses']) < 5 or student['gpa'] >= 3.0:
                    student['courses'].append(course_name)
                    print("\n------------------------")
                    print(f"| Class {course_name} added successfully! |")
                    print("------------------------\n")
                else:
                    print(
                        "Cannot register for more than 5 classes with GPA less than 3.0")
                return schedules
        print(f"No schedule found for {self.username}")

    def drop_class(self, course_name, schedules):
        for student in schedules:
            if student['name'] == self.username:
                student['courses'] = [
                    course for course in student['courses'] if course != course_name]
                print("\n------------------------")
                print(f"| Class {course_name} dropped successfully! |")
                print("------------------------\n")
                return schedules
        print(f"No schedule found for {self.username}")

    def view_classes(self, courses):
        print("------------------------")
        for course in courses:
            print("|", course.name, "|")
        print("------------------------")

    def has_completed(self, course_name):  # New method
        return any(course.name == course_name for course in self.completed_courses)

    def complete_course(self, course_name):  # New method
        self.schedule = [
            course for course in self.schedule if course.name != course_name]
        self.completed_courses.append(course_name)
