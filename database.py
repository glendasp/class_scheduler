import sqlite3
from models import Student, Course

# TODO: Needs a lot of exception handling!!!
# A general helper method that does all the dirty work might be useful.


class DatabaseManager:
    """Manages connecting and getting information from the database."""

    def __init__(self, filename):
        """Set up the connection to the database."""
        self.conn = sqlite3.connect(filename)

    def get_student(self, student_id):
        """Return a Student object if they exist, None otherwise."""
        cur = self.conn.cursor()
        query = 'SELECT ROWID, * FROM Student WHERE ROWID = ?'
        # cur.execute expects a tuple for the second argument.  You will get an
        # error if you only pass student_id.  Passing in (student_id, ) makes it
        # a single item tuple.  Another way to do it would be to pass in
        # tuple(student)
        cur.execute(query, (student_id, ))

        row = cur.fetchone()
        if row:
            return Student(row[0], row[1], row[2])

        return None

    def get_course(self, course_id):
        """Return a Course object if it exists, None otherwise."""
        cur = self.conn.cursor()
        query = 'SELECT ROWID, * FROM Course WHERE ROWID = ?'
        cur.execute(query, (course_id, ))

        row = cur.fetchone()
        if row:
            return Course(row[0], row[1])

        return None

    def get_courses_by_name(self, course_name):
        """Return a list of Courses that match the course_name."""
        cur = self.conn.cursor()
        # TODO: Query parameter might need some wildcards added.
        query = 'SELECT ROWID, * FROM Course WHERE UPPER(Course_Name) LIKE ?'
        cur.execute(query, (course_name.upper(), ))

        courses = []
        for row in cur:
            courses.append(Course(row[0], row[1]))

        return courses

    def register_course(self, student, course):
        """Register the Student to the Course."""
        cur = self.conn.cursor()
        query = 'INSERT INTO Student_Course VALUES (?, ?)'
        cur.execute(query, (student.id, course.id))
        self.conn.commit()
