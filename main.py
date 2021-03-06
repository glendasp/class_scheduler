"""
This class deals with the user interface and error checking of the input data
gives couple of menu options and define each option to perform an action.

"""

from database import DatabaseManager

db = DatabaseManager('School.db')
db.setup_db()


def main_menu(student):
    """
    Display menu for user, checks if the user input is an integer and does
    action basis option chosen.

    """

    menu_string = (
        '\n\t** MAIN MENU **\n'
        '\nStudent: {} {}\n'
        '\t1) Register Course\n'
        '\t2) Drop Course\n'
        '\t3) Display Schedule\n'
        '\t4) Quit\n'
        '\nEnter Selection'
    ).format(student.first_name, student.last_name)

    while True:
        menu_choice = get_user_int(menu_string, range(1, 5))

        if menu_choice == 1:
            register_course_menu(student)
        elif menu_choice == 2:
            drop_student_course_(student)
        elif menu_choice == 3:
            display_schedule(student)
        elif menu_choice == 4:
            break


def register_course_menu(student):
    """Sub-menu for register course option."""

    menu_string = (
        '\nREGISTER COURSE\n'
        '\t1) By Course ID\n'
        '\t2) Search for Course by Name\n'
        '\t3) Back\n'
        '\nEnter Selection'
    )

    # Loop to check the options entered by the user
    while True:
        menu_choice = get_user_int(menu_string, range(1, 4))

        if menu_choice == 1:
            course_id = get_user_int('Enter Course ID')
            course = db.get_course(course_id)
            if course:
                db.register_course(student, course)
                print('\n --> ' + student.first_name + ' was successfully added to the class <--')
            else:
                print('No course found with id:', course_id)
        elif menu_choice == 2:
            course = search_for_course(student)
            if course:
                db.register_course(student, course)
                print('\n --> ' + student.first_name + ' was successfully added to the class <--')
        elif menu_choice == 3:
            return


def drop_student_course_(student):
    """Drop a course based on the course id entered by the user."""

    student_course_list = db.get_course_by_student_id(student.id)

    # Print a meaningful message if the course list is empty.
    if len(student_course_list) == 0:
        print(student.full_name + " does not have any course in the list yet")
        return
    else:
        # Display registered courses for the student
        print("The current course list for " + student.full_name)
        for course in student_course_list:
            print("\t{}.{} ".format(course.id, course.name))
    while True:
        drop_question = 'Enter course id to drop from the given course list'
        drop_course_id = get_user_int(drop_question)
        Confirmation_Message = input("Do You want to drop " + db.get_course(drop_course_id).name + " from your course list(Y/N)?")
        if str(Confirmation_Message).upper() == 'Y':
            student_course_idlist = [course.id for course in student_course_list]
            if drop_course_id in student_course_idlist:
                db.drop_course(student.id, drop_course_id)
                print(str(db.get_course(drop_course_id).name) + " has been dropped from your current course list")
                break
            else:
                print(" No course found with that ID in the list !!! please check the list carefully")
        elif str(Confirmation_Message).upper() == 'N':
            return
        else:
            print("Invalid entry")
            continue
    return


def display_schedule(student):
    """Display the schedule for the current Student."""
    course_info = db.get_course_by_student_id(student.id)

    # Print a meaningful message if the course list is empty.
    if len(course_info) == 0:
        print(student.full_name + " does not have any course in the list yet")
    else:
        print("Your schedule for fall 2016:")
        for course in course_info:
            print("\t{} ({})".format(course.name, course.instructor.full_name))


def search_for_course(student):
    """Search for a course by name."""

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
        menu_string = '\nSelect a course\n'
        for n, course in enumerate(courses):
            menu_string += '\t{}) {}\n'.format(n + 1, course.name)
        menu_string += '\t{}) Back\n'.format(course_count + 1)
        menu_string += '\nSelect a Course'
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
    """
    Entry point which gets a Student and displays the name for the first time.
    Calls menu method if the input is valid from the user.

    """

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

    print('\n ** GoodBye! **')

main()
