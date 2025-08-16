from argparse import ArgumentParser

parent_parser = ArgumentParser(
    prog="safeParse",
    description="A command-line security toolkit that provides a unified interface to manage passwords, encrypt messages, and maintain secure access control.",
)

"""
    parent parser
    |    
auth_parser | -- subparser of parent parser
    |                 
user_auth_parser      |-- subparser of auth_parser
create_parser         |

"""
# subparser of parent parser
subparsers = parent_parser.add_subparsers(dest="command", required=True)

# user login parser
auth_parser = subparsers.add_parser("auth", help="Authentication-related commands")
auth_subparser = auth_parser.add_subparsers(dest="auth_command", required=True)
user_auth_parser = auth_subparser.add_parser(name="user", help="Login a user")
"""
# user creation parser
create_user_parser = auth_subparser.add_parser(
    name="create-user", help="Create a new user"
)

# user functionality parser
user_parser = subparsers.add_parser("user", help="user-related commands")
user_subparser = user_parser.add_subparsers(dest="user_command", required=True)
user_delete_parser = user_subparser.add_parser(
    name="delete", help="remove current user and all related things"
)
"""
# full feature parser
menu_parser = subparsers.add_parser("menu", help="menu for feature access")
