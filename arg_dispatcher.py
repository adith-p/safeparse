import shlex

from rich import print

from utils.user_auth import auth_command, is_authenticated
from arg_parsers.parent_parser import parent_parser
from utils.menu import menu_system, pass_menu, pass_opt_menu
from utils.passgen import gen_password

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

    # elif parser.command == "password":
    #     print(parser.echo)
    elif parser.command == "menu":
        opt = menu_system()
        if opt == 0:
            pass_opt = pass_menu()
            if pass_opt == 0:
                print(gen_password())
            elif pass_opt == 1:
                try:
                    cust_pass_option, pass_len = pass_opt_menu()
                except ValidationError:
                    print("[red] password need atleast 6 characters")
                    return True
                print(gen_password(length=pass_len, custom_list=cust_pass_option))

    return True
