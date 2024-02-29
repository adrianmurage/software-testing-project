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
        self.schedule = []
        self.completed_courses = []  # New attribute
        self.gpa = 0.0

    def register_for_class(self, course, system):
        if len(system.schedules.get(self.username, [])) < 5 or self.gpa >= 3.0:
            if course.add_student(self):
                system.register_for_class(self.username, course)
            else:
                print(f"The course {course.name} is full.")
        else:
            print("Cannot register for more than 5 classes with GPA less than 3.0")

    def view_schedule(self):
        print("------------------------")
        for course in self.schedule:
            print("|", course.name, "|")
        print("------------------------")

    def add_class(self, course):
        self.schedule.append(course)
        print("\n------------------------")
        print(f"| Class {course.name} added successfully! |")
        print("------------------------\n")

    def drop_class(self, course_name):
        for course in self.schedule:
            if course.name == course_name:
                course.remove_student(self)
                self.schedule.remove(course)
                break

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
