from simple_term_menu import TerminalMenu
from beaupy import confirm, prompt, select, select_multiple
from beaupy._internals import ValidationError


# added docstring using ai and refactored it, so that is why this is very distinct from other files
def show_main_menu():
    """Displays the main application menu and returns the user's choice.

    The menu provides top-level options for generating a password,
    managing existing passwords, or quitting the application.

    Returns:
        int: The index of the selected menu item.
             0: generate password
             1: view/save passwords
             2: quit
    """
    opts = ["generate password", "view/save passwords", "quit"]
    terminal_menu = TerminalMenu(opts, title="Main Menu")
    menu_entry = terminal_menu.show()
    return menu_entry


def show_password_type_menu():
    """Displays the password generation type menu.

    This menu allows the user to choose between generating a password
    with default settings or with custom-defined options.

    Returns:
        int: The index of the selected menu item.
             0: default
             1: custom
    """
    opts = ["default", "custom"]
    terminal_menu = TerminalMenu(opts, title="Select Password Type")
    menu_entry = terminal_menu.show()
    return menu_entry


def get_password_config():
    """Prompts the user for custom password configuration options.

    Asks the user for the desired password length and which character
    sets (uppercase, lowercase, symbols, numbers) to include.

    Raises:
        ValidationError: If the user provides a length less than or equal to 5.

    Returns:
        tuple[list[str], int]: A tuple containing:
            - A list of selected character type options (e.g., ['use uppercase']).
            - An integer for the desired password length.
    """
    opts = [
        "use uppercase",
        "use lowercase",
        "use symbols",
        "use numbers",
    ]

    # The `prompt` function will raise ValidationError on its own if the
    # validator condition is not met.
    pass_len = prompt(
        "Enter the length of the password",
        target_type=int,
        validator=lambda count: count > 5,
    )

    selected_opts = select_multiple(
        opts,
        tick_character="*",
        minimal_count=1,  # Require at least one option to be chosen
        title="Select character types to include:",
    )

    return (selected_opts, pass_len)
