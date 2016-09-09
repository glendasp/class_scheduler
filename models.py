"""These classes are used to help bundle the data from the database."""


class Student:
    def __init__(self, student_id, first_name, last_name):
        self.id = student_id
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Course:
    def __init__(self, course_id, name, instructor):
        self.id = course_id
        self.name = name
        self.instructor = instructor


class Instructor:
    def __init__(self, instructor_id, first_name, last_name):
        self.id = instructor_id
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
