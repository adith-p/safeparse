from prompt_toolkit import PromptSession
from rich import print
import time

from safeparse.core.dispatcher import dispatch


from safeparse.core.startup_fn import init_db
from safeparse.core.users.user_auth import create_user, is_authenticated
from safeparse.logging.logger import logger
from safeparse.core.users.user_auth import set_auth


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
    status = init_db()
    if not status:
        create_user()
    print("[bold magenta]🔐 Welcome to SafeParse[/bold magenta]")
    print("Type [bold] auth user [/bold] to continue")
    logger.info("Application started")
    session = PromptSession()

    INACTIVITY_TIME = 300
    last_time_out = time.time()
    while True:
        try:
            if is_authenticated():

                current_time = time.time()
                if (current_time - last_time_out) > float(INACTIVITY_TIME):
                    set_auth(False)
                    logger.warning("User session timed out due to inactivity.")
                    print(
                        "\n[bold yellow]Session timed out due to inactivity. Please log in again.[/bold yellow]"
                    )
                    break

#            last_time_out = time.time()
            prompt_text = "(auth-cli) " if is_authenticated() else "(un-auth) "
            text = session.prompt(prompt_text)
            last_time_out = time.time()
            if dispatch(text) is False:
                break

        except KeyboardInterrupt:

            last_time_out = time.time()
            continue
        except EOFError:
            break


if __name__ == "__main__":
    main()
