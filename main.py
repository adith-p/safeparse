from prompt_toolkit import PromptSession
from argparse import ArgumentParser
from rich import print


# from .utils.dispatcher import despatch
# from .utils.dispatcher import despatch

from arg_dispatcher import dispatch

# from arg_parsers.parent_parser import parent_parser
# from arg_parsers.login_parser import user_auth

from utils.user_auth import is_authenticated


# Interactive loop
def main():
    global authenticated_user
    print_this = """
         ███████  █████  ███████ ███████ ██████   █████  ██████  ███████ ███████
         ██      ██   ██ ██      ██      ██   ██ ██   ██ ██   ██ ██      ██
         ███████ ███████ █████   █████   ██████  ███████ ██████  ███████ █████
              ██ ██   ██ ██      ██      ██      ██   ██ ██   ██      ██ ██
         ███████ ██   ██ ██      ███████ ██      ██   ██ ██   ██ ███████ ███████
     """
    print(print_this)
    print("[bold magenta]🔐 Welcome to SafeParse[/bold magenta]")
    print("Type [bold]login --username <u> --password <p>[/bold] to continue")

    session = PromptSession()
    while True:
        try:
            prompt_text = "(auth-cli) " if is_authenticated() else "(unauth) "
            text = session.prompt(prompt_text)

            if dispatch(text) is False:
                break

        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == "__main__":
    main()
