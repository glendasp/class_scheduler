import sqlite3

sql_script = '''
CREATE TABLE Student (
  Firstname TEXT,
  Lastname TEXT
);

CREATE TABLE Course (
  Course_Name TEXT
);

CREATE TABLE Instructor (
  Firstname TEXT,
  Lastname TEXT
);

CREATE TABLE Student_Course (
  StudentID REFERENCES Student(ROWID),
  CourseID REFERENCES Course(ROWID)
);

CREATE TABLE Instructor_Course (
  InstructorID REFERENCES Instructor(ROWID),
  CourseID REFERENCES Course(ROWID)
);

INSERT into Student VALUES ('David', 'Oser');
INSERT into Student VALUES ('Diana', 'smith');
INSERT into Student VALUES ('Sarah', 'Mcarthy');
INSERT into Student VALUES ('chitra', 'Kakkar');

INSERT INTO Course VALUES ('Capstone');
INSERT INTO Course VALUES ('Java');
INSERT INTO Course VALUES ('C#');
INSERT INTO Course VALUES ('Python');

INSERT into Instructor VALUES ('Andy', 'Chrastek');
INSERT into Instructor VALUES ('Eric', 'Level');
INSERT into Instructor VALUES ('Clara', 'James');
INSERT into Instructor VALUES ('Joan', 'Carter');

'''

try:
    print('Creating tables')
    conn = sqlite3.connect('School.db')
    conn.executescript(sql_script)
except sqlite3.OperationalError as oe:
    print('Error:', oe)
    print("Database already exists..Aborting")
