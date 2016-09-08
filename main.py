from database import DatabaseManager

# TODO: Might need a redesign if we want to get rid of this global.
db = DatabaseManager('School.db')
db.setup_db()


def main_menu(student):
    menu_string = (
        '\nMAIN MENU\n'
        'Student: {} {}\n'
        '\t1) Register Course\n'
        '\t2)Drop Course\n'
        '\t3) Quit\n'
        'Enter Selection'
    ).format(student.first_name, student.last_name)

    while True:
        menu_choice = get_user_int(menu_string, range(1, 6))

        if menu_choice == 1:
            register_course_menu(student)
        elif menu_choice == 2:
            drop_student_course_(student)
        elif menu_choice == 3:
            break


def register_course_menu(student):
    menu_string = (
        '\nREGISTER COURSE\n'
        '\t1) By Course ID\n'
        '\t2) Search for Course by Name\n'
        '\t3) Back\n'
        'Enter Selection'
    )

    while True:
        menu_choice = get_user_int(menu_string, range(1, 4))

        if menu_choice == 1:
            course_id = get_user_int('Enter Course ID')
            course = db.get_course(course_id)
            if course:
                db.register_course(student, course)
            else:
                print('No course found with id:', course_id)
        elif menu_choice == 2:
            course = search_for_course()
            if course:
                db.register_course(student, course)
        elif menu_choice == 3:
            return


def drop_student_course_(student):
    drop_question = 'Enter course id to drop from the course list'
    while True:
        drop_course_id = get_user_int(drop_question, None)
        courses_drop = db.drop_course(student.id, drop_course_id)
        print(courses_drop + "has been dropped from your current course list")
        return


def search_for_course():
    course_name = get_user_string('Enter Course Name')
    courses = db.get_courses_by_name(course_name)

    if not courses:
        print('No course with that name found.')
        # Leave early.  The user can come back to search unless we want to ask
        # them to try again.  This gets messy pretty fast unless we figure out
        # a better way to do these menus.
        return

    while True:
        course_count = len(courses)

        menu_string = 'Select a course\n'
        for n, course in enumerate(courses):
            menu_string += '\t{}) {}\n'.format(n + 1, course.name)
        menu_string += '\t{}) Back\n'.format(course_count + 1)
        menu_string += 'Select a Course'

        menu_choice = get_user_int(menu_string, range(1, course_count + 2))

        if menu_choice <= course_count:
            return courses[menu_choice - 1]
        else:
            return None


def get_user_int(message, valid_range=None):
    """Return an integer from the user

    Args:
        message (str): Message to prompt user with.
        valid_range (iter or list of ints): A range or list of valid numbers.

    """
    while True:
        user_input = input('{}: '.format(message))

        # Type validation
        try:
            number = int(user_input)
        except ValueError:
            print('You must enter a whole number.')
            continue

        # Range validation
        if valid_range and number not in valid_range:
            _min = min(valid_range)
            _max = max(valid_range)
            print('You must enter a number from {} to {}.'.format(_min, _max))
            continue

        # All tests passed
        return number


def get_user_string(message):
    """Return a string from the user.

    Args:
        message (str): Message to prompt the user with.

    """

    while True:
        user_input = input('{}: '.format(message))
        # This is a bad way to check if the user input is not empty.
        # It will be True if the user enters spaces, tabs, etc.
        if user_input:
            return user_input
        else:
            print('You must enter something.')


def main():
    student = None

    while True:
        student_id = get_user_int('Enter Student ID')
        student = db.get_student(student_id)
        if not student:
            print('No student found with id:', student_id)
            continue
        break

    # Even though it's pretty much guaranteed that we will have a student if we
    # reach this line because the user will will be stuck in an infinite loop
    # if they cannot provide a valid student id, I am still checking if it's not
    # none to get rid of the warning that it might be referenced before
    # assignment.  Whew, that was a long sentence.
    if student:
        main_menu(student)

    print('GoodBye!')

main()
