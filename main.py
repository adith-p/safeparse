from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.patch_stdout import patch_stdout


from rich import print


from arg_dispatcher import dispatch


from utils.user_auth import is_authenticated
from utils.startup import init_db


# Interactive loop
def main():
    print_this = """
         ███████  █████  ███████ ███████ ██████   █████  ██████  ███████ ███████
         ██      ██   ██ ██      ██      ██   ██ ██   ██ ██   ██ ██      ██
         ███████ ███████ █████   █████   ██████  ███████ ██████  ███████ █████
              ██ ██   ██ ██      ██      ██      ██   ██ ██   ██      ██ ██
         ███████ ██   ██ ██      ███████ ██      ██   ██ ██   ██ ███████ ███████
     """
    print(print_this)
    init_db()
    print("[bold magenta]🔐 Welcome to SafeParse[/bold magenta]")
    print("Type [bold] auth user [/bold] to continue")
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
