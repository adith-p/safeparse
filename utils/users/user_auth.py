from rich import print


from prompt_toolkit import PromptSession
import bcrypt
from getpass import getpass
from uuid import uuid4

from utils.database_controllers import UserDbController

user_request: dict[str, bool | None] = {
    "username": None,
    "user_id": None,
    "is_authenticated": False,
}


def password_hash(password, salt):
    return bcrypt.hashpw(password.encode(), salt)


def hash_password(password):
    password_salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), password_salt), password_salt


def verify_password(psw, hashed_psw):
    return bcrypt.checkpw(psw.encode(), hashed_psw)


def login():
    session = PromptSession()

    username = session.prompt("Username > ").strip()
    if not username:
        print(" Username cannot be empty.")
        return None

    password = getpass("Password > ").strip()
    if not password:
        print("Password cannot be empty.")
        return None
    # parser = parent_parser.parse_args(arg)
    # return authenticate(username=parser.username, password=parser.password)
    return authenticate(username=username, password=password)


def authenticate(username, password) -> bool:
    # global user_authenticated

    user_data = UserDbController().get_user(username)

    if user_data is None:
        print("user does not exist")
        return False

    if user_data[1] == username:

        hashed_password = password_hash(password=password, salt=user_data[3])
        if verify_password(password, hashed_password):
            user_request["is_authenticated"] = True
            user_request["username"] = username
            user_request["user_id"] = user_data[0]

            return True
        print("[red] password or username is incorrect [/red]")
    # except Exception:
    #     print(
    #         "[red] user does not exist [/red] try - [purple] auth create-user [/purple]"
    #     )
    return False


def create_user(parser):

    db = UserDbController()
    session = PromptSession()

    # Check if user already exists
    username = session.prompt("Username > ").strip()
    if username:
        if db.get_user(username):
            print("['red']Username already exists.['/red']")
            return False
    else:
        print("[red] username can't be empty [/red]")
        return False

    password = getpass("Password > ").strip()
    if not password:
        print("['red']Password cannot be empty.['/red']")
        return False

    password_hash, password_salt = hash_password(password)
    user_id = str(uuid4())
    curr = UserDbController().create_user(
        user_id, username, password_hash, password_salt
    )

    return True


def is_authenticated() -> bool:
    return user_request["is_authenticated"]


def get_current_username() -> str | None:
    return user_request["username"]


def get_current_user_id() -> str | None:
    return user_request["user_id"]


def auth_command(parser):

    if parser.auth_command == "user":

        if login():
            print("[green] user authenticated [/green]")
        else:
            return False

    elif parser.auth_command == "create-user":
        if create_user(parser):
            print(
                "[green] user created successfully [/green] try [bold magenta] auth [/bold magenta]"
            )
        else:
            print("[red] user already exist[/red] try - [purple] auth user [/purple]")
            return False

    return True
