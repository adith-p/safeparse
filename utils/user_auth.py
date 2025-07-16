from arg_parsers.login_parser import parent_parser, auth_subparser
from rich import print

from prompt_toolkit import PromptSession


db = {"admin": "123"}

user_authenticated = None


def login(parser):

    # parser = parent_parser.parse_args(arg)
    return authenticate(username=parser.username, password=parser.password)


def authenticate(username, password) -> bool:
    global user_authenticated
    if username in db.keys():
        if password == db[username]:
            user_authenticated = True
            return True
        return False


def create_user(parser):

    # parser = parent_parser.parse_args(arg)

    if parser.username in db.keys():
        print("[red] username already exist [/red]")
        return False
    session = PromptSession()
    password = session.prompt(" Password > ")
    db[parser.username] = password
    return True


def is_authenticated() -> bool:
    return user_authenticated


def hash_password():
    pass


def verfy_password():
    pass


def auth_command(parser):

    if parser.auth_command == "user":

        if login(parser):
            print("[green] user authenticated [/green]")
        else:
            print("[red] invalid [/red]")
            return False

    elif parser.auth_command == "create-user":
        if create_user(parser):
            print(
                "[green] user created successfully [/green] try [bold magenta] auth [/bold magenta]"
            )
        else:
            print("[red] user already exist[/red]")
            return False

    # elif sub_cmd == "--help":
    #     print(parent_parser.add_help())
