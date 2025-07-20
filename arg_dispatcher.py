import shlex

from rich import print

from utils.menu import get_password_config, show_main_menu, show_password_type_menu
from utils.user_auth import auth_command, is_authenticated
from arg_parsers.parent_parser import parent_parser

from utils.passgen import gen_password

# from utils.user_auth import user_command

from beaupy._internals import ValidationError


def dispatch(raw_string):
    tokens = shlex.split(raw_string)

    if not tokens:
        return

    parser = parent_parser.parse_args(tokens)

    if parser.command != "auth":
        if not is_authenticated():
            print("[red] user should be authenticated first [/red]")
            return

    if parser.command == "auth":
        auth_command(parser)

    # if parser.command == "user":
    #     # NOTE:- once the password vault have been set up work on this
    #     user_command(parser)

    elif parser.command == "menu":
        opt = show_main_menu()

        if opt == 0:
            pass_type = show_password_type_menu()

            if pass_type == 0:
                print(gen_password())

            elif pass_type == 1:
                try:
                    custom_options, pass_len = get_password_config()
                    print(gen_password(length=pass_len, custom_list=custom_options))
                except ValidationError:
                    print("[red]Password must be at least 6 characters long.")
                    return True

        # Option 1: View/Save Passwords
        # if opt == 1:
        #     storage_action = show_password_storage_menu()

        #     # View passwords
        #     if storage_action == 0:
        #         print(storage_action) # Replace with view logic

        #     # Save password
        #     if storage_action == 1:
        #         print(storage_action) # Replace with save logic

        return True
