import sqlite3
from models import Student, Course, Instructor

# TODO: Needs a lot of exception handling!!!
# A general helper method that does all the dirty work might be useful.


class DatabaseManager:
    """Manages connecting and getting information from the database."""

    def __init__(self, filename):
        """Set up the connection to the database."""
        self.conn = sqlite3.connect(filename)

    def setup_db(self):
        sql_script = '''
            CREATE TABLE Student (
              Firstname TEXT,
              Lastname TEXT
            );

            CREATE TABLE Course (
              Name TEXT,
              InstructorID REFERENCES Instructor(ROWID)
            );

            CREATE TABLE Instructor (
              Firstname TEXT,
              Lastname TEXT
            );

            CREATE TABLE Student_Course (
              StudentID REFERENCES Student(ROWID),
              CourseID REFERENCES Course(ROWID)
            );

            INSERT INTO Student VALUES ('David', 'Oser');
            INSERT INTO Student VALUES ('Diana', 'smith');
            INSERT INTO Student VALUES ('Sarah', 'Mcarthy');
            INSERT INTO Student VALUES ('Chitra', 'Kakkar');
            INSERT INTO Student VALUES ('Glenda', 'Pinho');
            INSERT INTO Student VALUES ('Eva', 'Mendes');
            INSERT INTO Student VALUES ('Mason', 'Elmore');
            INSERT INTO Student VALUES ('Yannick', 'Idrissa');
            INSERT INTO Student VALUES ('Marian', 'Abshir');
            INSERT INTO Student VALUES ('Branden', 'Adams');
            INSERT INTO Student VALUES ('Anna', 'Dudda');
            INSERT INTO Student VALUES ('Federico', 'Fernandez Diaz');
            INSERT INTO Student VALUES ('Joe', 'Lee');
            INSERT INTO Student VALUES ('Malcolm', 'Leehan');
            INSERT INTO Student VALUES ('Timothy', 'Milligan');
            INSERT INTO Student VALUES ('Robert', 'Williams');
            INSERT INTO Student VALUES ('Malcolm', 'Leehan');

            INSERT INTO Course VALUES ('Capstone', 1);
            INSERT INTO Course VALUES ('Java',2);
            INSERT INTO Course VALUES ('C#', 3);
            INSERT INTO Course VALUES ('Python', 4);
            INSERT INTO Course VALUES ('SQL', 1);
            INSERT INTO Course VALUES ('Software Development Capstone', 1);
            INSERT INTO Course VALUES ('Microsoft Windows Operating Systems', 5);
            INSERT INTO Course VALUES ('Programming Logic and Design', 6);

            INSERT INTO Instructor VALUES ('Andy', 'Chrastek');
            INSERT INTO Instructor VALUES ('Eric', 'Level');
            INSERT INTO Instructor VALUES ('Clara', 'James');
            INSERT INTO Instructor VALUES ('Joan', 'Carter');
            INSERT INTO Instructor VALUES ('Richard', 'Pollak');
            INSERT INTO Instructor VALUES ('Eric', 'Level');
        '''

        try:
            print('Creating tables...')
            self.conn = sqlite3.connect('School.db')
            self.conn.executescript(sql_script)
            print("Table successfully created")
        except sqlite3.OperationalError as oe:
            print('Error:', oe)

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
            student_id, first_name, last_name = (row[0], row[1], row[2])
            return Student(student_id, first_name, last_name)

        return None

    def get_course(self, course_id):
        """Return a Course object if it exists, None otherwise."""
        cur = self.conn.cursor()
        query = 'SELECT ROWID, * FROM Course WHERE ROWID = ?'
        cur.execute(query, (course_id, ))

        row = cur.fetchone()
        if row:
            course_id, course_name, instructor_id = (row[0], row[1], row[2])
            instructor = self.get_instructor(instructor_id)
            return Course(course_id, course_name, instructor)

        return None

    def get_courses_by_name(self, course_name):
        """Return a list of Courses that match the course_name."""
        cur = self.conn.cursor()
        # TODO: Query parameter might need some wildcards added.
        query = 'SELECT ROWID, * FROM Course WHERE UPPER(Name) LIKE ?'
        cur.execute(query, (course_name.upper(), ))

        courses = []
        for row in cur:
            course_id, course_name, instructor_id = (row[0], row[1], row[2])
            instructor = self.get_instructor(instructor_id)
            courses.append(Course(course_id, course_name, instructor))

        return courses

    def get_course_by_student_id(self, student_id):
        """Return a student's list of Courses """
        cur = self.conn.cursor()
        query = 'SELECT * FROM Student_Course WHERE StudentID LIKE ?'
        cur.execute(query, (student_id,))

        courses_list = []
        for row in cur.fetchall():
            course_id = row[1]
            courses_list.append(self.get_course(course_id))

        return courses_list

    def get_instructor(self, instructor_id):
        """Return an Instructor object if it exists, None otherwise."""
        cur = self.conn.cursor()
        query = 'SELECT ROWID, * FROM Instructor WHERE ROWID = ?'
        cur.execute(query, (instructor_id, ))

        row = cur.fetchone()
        if row:
            instructor_id, first_name, last_name = (row[0], row[1], row[2])
            return Instructor(instructor_id, first_name, last_name)

        return None

    def register_course(self, student, course):
        """Register the Student to the Course."""
        cur = self.conn.cursor()
        query = 'INSERT INTO Student_Course VALUES (?, ?)'
        cur.execute(query, (student.id, course.id))
        self.conn.commit()

    def drop_course(self, studentID, CourseID):
        """ Drop the course from the course list for the student."""
        cur = self.conn.cursor()
        query = ('DELETE FROM Student_Course '
                 '  WHERE CourseID = ? '
                 '  AND  StudentID = ?')
        cur.execute(query, (CourseID, studentID))
        self.conn.commit()
