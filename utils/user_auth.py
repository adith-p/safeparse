from arg_parsers.login_parser import user_auth_parser, parent_parser
from rich import print

from prompt_toolkit import PromptSession


db = {"admin": "123"}


def login(arg):
    parser = parent_parser.parse_args(arg)

    return authenticate(username=parser.username, password=parser.password)


def authenticate(username, password) -> bool:
    if username in db.keys():
        if password == db[username]:
            return True


def create_user(arg):

    parser = parent_parser.parse_args(arg)

    if parser.username in db.keys():
        print("[red] username already exist [/red]")
        return False
    session = PromptSession()
    password = session.prompt(" Password > ")
    db[parser.username] = password
    return True
