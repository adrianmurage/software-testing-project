import unittest
from user import Admin, Student
from unittest.mock import patch
from io import StringIO

class Course:
    def __init__(self, name):
        self.name = name

class TestAdmin(unittest.TestCase):
    def setUp(self):
        self.admin = Admin('admin', 'password')
        self.course1 = Course('Math')
        self.course2 = Course('English')
        self.courses = [self.course1]

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_course(self, mock_stdout):
        self.admin.add_course(self.course2, self.courses)
        self.assertIn(self.course2, self.courses)
        self.assertIn('Course English added successfully', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_course(self, mock_stdout):
        self.admin.update_course('Math', self.course2, self.courses)
        self.assertIn(self.course2, self.courses)
        self.assertNotIn(self.course1, self.courses)
        self.assertIn('Course Math updated successfully', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_course(self, mock_stdout):
        self.admin.delete_course('Math', self.courses)
        self.assertNotIn(self.course1, self.courses)
        self.assertIn('Course Math deleted successfully', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_courses(self, mock_stdout):
        self.admin.view_courses(self.courses)
        self.assertIn('Math', mock_stdout.getvalue())

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student('student1', 'password')
        self.schedules = [
            {
                'name': 'student1',
                'courses': ['Math', 'English'],
                'completed_courses': ['History'],
                'gpa': 3.5
            },
            {
                'name': 'student2',
                'courses': ['Science', 'Geography'],
                'completed_courses': ['Math'],
                'gpa': 2.5
            }
        ]

    @patch('sys.stdout', new_callable=StringIO)
    def test_view_schedule(self, mock_stdout):
        self.student.view_schedule(self.schedules)
        self.assertIn('Schedule for student1', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_class(self, mock_stdout):
        self.student.add_class('Science', self.schedules)
        self.assertIn('Class Science added successfully', mock_stdout.getvalue())
        self.assertIn('Science', self.schedules[0]['courses'])

    @patch('sys.stdout', new_callable=StringIO)
    def test_drop_class(self, mock_stdout):
        self.student.drop_class('Math', self.schedules)
        self.assertIn('Class Math dropped successfully', mock_stdout.getvalue())
        self.assertNotIn('Math', self.schedules[0]['courses'])

if __name__ == '__main__':
    unittest.main()