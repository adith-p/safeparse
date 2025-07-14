import shlex

from rich import print

from utils.user_auth import auth_command, is_authenticated
from arg_parsers.parent_parser import parent_parser


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

    return True
