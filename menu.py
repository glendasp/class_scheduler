from collections import namedtuple

MenuItem = namedtuple('MenuItem', ['text', 'function', 'args', 'kwargs'])


def run_menu(title, items, add_exit=True, exit_text='Exit'):
    """Display a list of options for the user to choose from.

    Args:
        title (str): Text to display at the top of the menu.
        items (tuple of MenuItem): List of menu options.
        add_exit (bool): Add an exit option the the end of the list.
        exit_text (str): Text to be displayed in the back option.

    """

    def build_menu():
        """Return the menu string.

        An example menu string looks something like this:
            Main Menu
                1) Option One
                2) Option Two
                3) Exit
            Enter Selection:

        """

        menu_string = title + '\n'
        for i, item in enumerate(items):
            menu_string += '\t{}) {}\n'.format(i + 1, item.text)
        if add_exit:
            menu_string += '\t{}) {}\n'.format(len(items) + 1, exit_text)
        menu_string += 'Enter Selection'

        return menu_string

    menu = build_menu()
    total_options = len(items) + 1 if add_exit else len(items)
    while True:
        choice = get_user_int(menu, range(1, total_options + 1))
        if choice <= len(items):
            selection = items[choice - 1]
            selection.function(*selection.args, **selection.kwargs)
        elif choice == len(items) + 1:
            break


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


if __name__ == '__main__':
    def hello_world(name='World'):
        message = 'Hello, {}!'.format(name)
        print(message)

    option_one = MenuItem('Hello, World!', hello_world, [], {})
    option_two = MenuItem('Hello, Mason!', hello_world, ['Mason'], {})

    run_menu('Menu Demo', (option_one, option_two))
