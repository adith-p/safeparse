from prompt_toolkit import PromptSession

from rich import print


from dispatcher import dispatch


from utils.startup_fn import init_db
from utils.users.user_auth import is_authenticated
from utils.event_logging.logger import logger


# Interactive loop
def main():
    # NOTE: .log can be tampered with as of now so, once the encryption module is set up i will encrypt and hash the .log file
    logger.info("Application starting...")
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
    logger.info("Application started")
    session = PromptSession()
    while True:
        try:

            prompt_text = "(auth-cli) " if is_authenticated() else "(un-auth) "
            text = session.prompt(prompt_text)

            if dispatch(text) is False:
                break

        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == "__main__":
    main()
