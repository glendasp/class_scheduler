"""Plain-old objects for handling information from the database."""


class Course:
    """Information about a course.

    Args:
        id (int): Course ID
        title (str): Name of the course.
        instructor_name (int): Instructor first and last name.
        days (list of str): Days when the course happens.
        time (str): Time of day for the course.

    """


class CourseSchedule:
    """Information about a student's course schedule.

    Args:
        student_name (str): Student's first and last name.
        courses (list of :obj:`course`):

    """
