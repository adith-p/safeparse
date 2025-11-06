from simple_term_menu import TerminalMenu
from beaupy import prompt, select_multiple


# added docstring using AI and refactored it, so that is why this is very distinct from other files
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
    opts = [
        "Generate password",
        "Manage passwords",
        "View logs",
        "Encryption",
        "Quit",
    ]
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
        # title="Select character types to include:",
    )

    return (selected_opts, pass_len)


def show_password_storage_menu():
    """Displays the password storage and retrieval menu.

    This menu allows the user to choose between viewing previously saved
    passwords or saving a new one.

    Returns:
        int: The index of the selected menu item.
             0: view
             1: save
             2: update
             3:delete
    """

    opts = [
        "view",
        "save",
        "update",
        "delete",
    ]
    terminal_menu = TerminalMenu(opts, title="Password Storage")
    menu_entry = terminal_menu.show()
    return menu_entry


def update_password_menu():
    """Displays the password update menu.

    This menu allows the user to choose which field of a saved password
    entry they want to update.

    Returns:
        int: The index of the selected menu item.
             0: username
             1: notes
             2: password
             3: quit
    """
    opts = [
        "login_username",
        "notes",
        "password",
    ]

    selected_opts = select_multiple(
        opts,
        tick_character="*",
        minimal_count=1,  # Require at least one option to be chosen
        # title="Select character types to include:",
    )
    return selected_opts


def show_enc_menu():
    opts = [
        "Key management",
        "Encrypt Things",
        "decrypt things",
        "contacts",
    ]

    terminal_menu = TerminalMenu(opts, title="Encryption functionalities")
    terminal_enc = terminal_menu.show()

    return terminal_enc


def show_enc_km_menu():
    opts = [
        "list public keys",
        "generate new key-pairs",
        "export public key",
        "import public key",
        "delete key",
        "revoke key",
    ]

    terminal_menu = TerminalMenu(opts, title="key management menu")
    terminal_enc = terminal_menu.show()
    return terminal_enc


def show_enc_edt_menu() -> int:
    opts = [
        "text messages",
        "files",
    ]

    terminal_menu = TerminalMenu(opts, title="encryption and decryption menu")
    terminal_enc = terminal_menu.show()
    return terminal_enc


def show_enc_contacts_menu() -> int:
    opts = [
        "view contacts",
        "add contacts",
        "update contacts",
        "delete contacts",
    ]

    terminal_menu = TerminalMenu(opts, title="contact menu")
    terminal_enc = terminal_menu.show()
    return terminal_enc


def show_key_length_menu():
    opts = [
        "RSA, 4096 bits (Recommended)",
        "RSA, 2048 bits (Good for compatibility)",
        "ECC (Elliptic Curve Cryptography)",
    ]
    terminal_menu = TerminalMenu(opts, title="key type and size menu")
    terminal_enc = terminal_menu.show()
    return terminal_enc


def show_key_menu(opts):
    key_menu = TerminalMenu(opts, title="Select the public/private key")
    key_selection = key_menu.show()
    return key_selection


def show_file_to_encrypt_menu(opts: list):
    key_menu = TerminalMenu(opts, title="Choose a file to encrypt")
    key_selection = key_menu.show()
    return key_selection


# encryption + contact display/selection
def show_available_contacts(opts: list):
    key_menu = TerminalMenu(opts, title="select the contact")
    key_selection = key_menu.show()
    return key_selection


def show_available_trust_level():
    opts = ["full", "never", "expired"]
    key_menu = TerminalMenu(
        opts, title="Enter a trust level for the imported key")
    key_selection = key_menu.show()
    return key_selection


def show_contact_fields():
    opts = [
        "contact name",
        "contact email",
        "public key fingerprint",
    ]
    selected_opts = select_multiple(opts, tick_character="*", minimal_count=1)
    return selected_opts


def show_avail_passwords(opts: list):
    psw_menu = TerminalMenu(opts, title="select a password id")
    psw_selection = psw_menu.show()
    return psw_selection
