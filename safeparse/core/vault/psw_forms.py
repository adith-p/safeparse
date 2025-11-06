from rich import print
from prompt_toolkit import PromptSession


def get_psw_form() -> tuple[str, str, str] | None:
    session = PromptSession()
    password = session.prompt("password > ").strip()
    username = session.prompt("username > ").strip()
    note = session.prompt("Note > ").strip()
    if note == "" and username == "":
        print("[bold green]username, note can't be empty[/bold green]")
        return None
    if password == "":
        print("[bold green] Password can't be empty[/bold green]")
    return (
        password,
        username,
        note,
    )


def view_psw_form() -> tuple[str, str]:
    session = PromptSession()
    search_params = session.prompt("search params >")

    return search_params


def request_password_id():
    session = PromptSession()
    password_id = session.prompt("password id > ")
    return password_id


def update_psw_form(attribute: str) -> tuple[str, str]:
    session = PromptSession()
    attribute_prompt = session.prompt(f"{attribute} > ")
    return attribute_prompt
