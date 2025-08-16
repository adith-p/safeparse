from typing import Any, TypedDict

from rich import print


from prompt_toolkit import PromptSession
import bcrypt
from getpass import getpass
from uuid import uuid4

from utils.database_controllers import UserDbController
from utils.event_logging.logger import logger


class UserReuest(TypedDict):
    username: str | None
    user_id: str | None
    is_authenticated: bool


user_request: UserReuest = {
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


def login() -> tuple[bool, Any] | None:
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
    return authenticate(username=username, password=password), username


def authenticate(username, password) -> bool:
    # global user_authenticated
    user_data = UserDbController().get_user_by_username(username)
    # user_data = UserDbController().get_user(username)

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


def create_user():

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

    psw_hash, password_salt = hash_password(password)
    user_id = str(uuid4())
    curr = UserDbController().create_user(
        user_id, username, psw_hash, password_salt
    )

    return True, username


def is_authenticated() -> bool | None:
    return user_request["is_authenticated"]


def set_auth(flag: bool):
    user_request["is_authenticated"] = flag


def get_current_username() -> str | None:
    return user_request["username"]


def get_current_user_id() -> str | None:
    return user_request["user_id"]


def auth_command(parser):

    if parser.auth_command == "user":
        login_object = login()
        if login_object[0]:
            print("[green] user authenticated [/green]")
            logger.info("Authentication successful for user: '%s'", login_object[1])
        else:
            logger.warning("user authentication failed for user: '%s'", login_object[1])
            return False

    elif parser.auth_command == "create-user":
        user_creation_object = create_user()
        if user_creation_object[0]:
            print(
                "[green] user created successfully [/green] try [bold magenta] auth [/bold magenta]"
            )
            logger.info("user created with username %s", get_current_username())
        else:
            print("[red] user already exist[/red] try - [purple] auth user [/purple]")
            logger.warning(
                "Failed to create user: username '%s' already exists.",
                user_creation_object[1],
            )
            return False

    return True
