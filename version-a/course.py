class Course:
    def __init__(self, name, is_open, prerequisite, capacity):
        self.name = name
        self.is_open = is_open
        self.prerequisite = prerequisite
        self.capacity = capacity
        self.students = []  # New attribute

    def add_student(self, student):
        if len(self.students) < self.capacity:
            self.students.append(student)
            return True
        else:
            return False

    def remove_student(self, student):
        self.students.remove(student)