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
              StudentNum INT PRIMARY KEY,
              FirstName TEXT NOT NULL,
              LastName TEXT NOT NULL
            );

            CREATE TABLE Course (
              CourseNum INT PRIMARY KEY,
              Name TEXT NOT NULL,
              InstructorNum INT,
              FOREIGN KEY (InstructorNum) REFERENCES Instructor
            );

            CREATE TABLE Instructor (
              InstructorNum INT PRIMARY KEY,
              FirstName TEXT NOT NULL,
              LastName TEXT NOT NULL
            );

            CREATE TABLE Student_Course (
              StudentNum INT NOT NULL,
              CourseNum INT NOT NULL,
              PRIMARY KEY (StudentNum, CourseNum),
              FOREIGN KEY (StudentNum) REFERENCES Student,
              FOREIGN KEY (CourseNum) REFERENCES Course
            );

            INSERT INTO Student VALUES (1, 'David', 'Oser');
            INSERT INTO Student VALUES (2, 'Diana', 'smith');
            INSERT INTO Student VALUES (3, 'Sarah', 'Mcarthy');
            INSERT INTO Student VALUES (4, 'Chitra', 'Kakkar');
            INSERT INTO Student VALUES (5, 'Glenda', 'Pinho');
            INSERT INTO Student VALUES (6, 'Eva', 'Mendes');
            INSERT INTO Student VALUES (7, 'Mason', 'Elmore');
            INSERT INTO Student VALUES (8, 'Yannick', 'Idrissa');
            INSERT INTO Student VALUES (9, 'Marian', 'Abshir');
            INSERT INTO Student VALUES (10, 'Branden', 'Adams');
            INSERT INTO Student VALUES (11, 'Anna', 'Dudda');
            INSERT INTO Student VALUES (12, 'Federico', 'Fernandez Diaz');
            INSERT INTO Student VALUES (13, 'Joe', 'Lee');
            INSERT INTO Student VALUES (14, 'Malcolm', 'Leehan');
            INSERT INTO Student VALUES (15, 'Timothy', 'Milligan');
            INSERT INTO Student VALUES (16, 'Robert', 'Williams');
            INSERT INTO Student VALUES (17, 'Malcolm', 'Leehan');

            INSERT INTO Course VALUES (1, 'Capstone', 1);
            INSERT INTO Course VALUES (2, 'Java',2);
            INSERT INTO Course VALUES (3, 'C#', 3);
            INSERT INTO Course VALUES (4, 'Python', 4);
            INSERT INTO Course VALUES (5, 'SQL', 1);
            INSERT INTO Course VALUES (6, 'Software Development Capstone', 1);
            INSERT INTO Course VALUES (7, 'Microsoft Windows Operating Systems', 5);
            INSERT INTO Course VALUES (8, 'Programming Logic and Design', 6);

            INSERT INTO Instructor VALUES (1, 'Andy', 'Chrastek');
            INSERT INTO Instructor VALUES (2, 'Eric', 'Level');
            INSERT INTO Instructor VALUES (3, 'Clara', 'James');
            INSERT INTO Instructor VALUES (4, 'Joan', 'Carter');
            INSERT INTO Instructor VALUES (5, 'Richard', 'Pollak');
            INSERT INTO Instructor VALUES (6, 'Eric', 'Level');

            INSERT INTO Student_Course VALUES (4, 5);
            INSERT INTO Student_Course VALUES (4, 6);
            INSERT INTO Student_Course VALUES (5, 5);
            INSERT INTO Student_Course VALUES (5, 6);
            INSERT INTO Student_Course VALUES (8, 6);
            INSERT INTO Student_Course VALUES (8, 7);
            INSERT INTO Student_Course VALUES (7, 6);
            INSERT INTO Student_Course VALUES (7, 8);
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
        query = 'SELECT * FROM Student WHERE StudentNum = ?'
        # cur.execute expects a tuple for the second argument.  You will get an
        # error if you only pass student_id.  Passing in (student_id, ) makes it
        # a single item tuple.  Another way to do it would be to pass in
        # tuple(student)
        cur.execute(query, (student_id,))

        row = cur.fetchone()
        if row:
            student_id, first_name, last_name = (row[0], row[1], row[2])
            return Student(student_id, first_name, last_name)

        return None

    def get_course(self, course_id):
        """Return a Course object if it exists, None otherwise."""
        cur = self.conn.cursor()
        query = (
            'SELECT CourseNum, Name, Course.InstructorNum, FirstName, LastName '
            'FROM Course '
            'JOIN Instructor ON Course.InstructorNum = Instructor.InstructorNum '
            'WHERE CourseNum = ?')
        cur.execute(query, (course_id,))

        row = cur.fetchone()
        if row:
            course_id, course_name = (row[0], row[1])
            instructor_id, first_name, last_name = (row[2], row[3], row[4])
            instructor = Instructor(instructor_id, first_name, last_name)
            return Course(course_id, course_name, instructor)

        return None

    def get_courses_by_name(self, course_name):
        """Return a list of Courses that match the course_name."""
        cur = self.conn.cursor()
        # TODO: Query parameter might need some wildcards added.
        query = (
            'SELECT CourseNum, Name, Course.InstructorNum, FirstName, LastName '
            'FROM Course '
            'JOIN Instructor ON Course.InstructorNum = Instructor.InstructorNum '
            'WHERE UPPER(Name) LIKE ?'
        )
        cur.execute(query, (course_name.upper(),))

        courses = []
        for row in cur:
            course_id, course_name = (row[0], row[1])
            instructor_id, first_name, last_name = (row[2], row[3], row[4])
            instructor = Instructor(instructor_id, first_name, last_name)
            courses.append(Course(course_id, course_name, instructor))

        return courses

    def get_course_by_student_id(self, student_id):
        """Return a student's list of Courses """
        cur = self.conn.cursor()
        query = 'SELECT * FROM Student_Course WHERE StudentNum LIKE ?'
        cur.execute(query, (student_id,))

        courses_list = []
        for row in cur.fetchall():
            course_id = row[1]
            courses_list.append(self.get_course(course_id))

        return courses_list

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
                 '  WHERE CourseNum = ? '
                 '  AND  StudentNum = ?')
        cur.execute(query, (CourseID, studentID))
        self.conn.commit()
