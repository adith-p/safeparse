import shlex

from rich import print

from utils.user_auth import login, create_user


def dispatch(command):
    tokens = shlex.split(command)

    if not tokens:
        return
    cmd = tokens[0]
    args = tokens[1:]

    if cmd == "auth":
        if login(args):
            print("[green] user authenticated [/green]")
        else:
            print("[red] invalid [/red]")
            return False

    elif cmd == "create-user":
        if create_user(args):
            print(
                "[green] user created successfully [/green] try [bold magenta] auth [/bold magenta]"
            )
        else:
            print("[red] user already exist[/red]")
            return False

    return True
