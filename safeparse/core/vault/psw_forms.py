from typing import Any

from prompt_toolkit import PromptSession


def get_psw_form() -> tuple[str, str, str]:
    session = PromptSession()
    password = session.prompt("password > ")
    username = session.prompt("username > ")
    note = session.prompt("Note > ")
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
