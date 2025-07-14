from .parent_parser import parent_parser


# creating a subparser for a parent parser
"""
    parent parser
    |    
auth_parser | -- subparser of parent parser
    |                 
user_auth_parser      |-- subparser of auth_parser
create_parser         |

"""


subparsers = parent_parser.add_subparsers(dest="command", required=True)

# subparser of parent parser
auth_parser = subparsers.add_parser("auth", help="Authentication-related commands")
auth_subparser = auth_parser.add_subparsers(dest="auth_command", required=True)

# user login parser
user_auth_parser = auth_subparser.add_parser(name="user", help="Login a user")
user_auth_parser.add_argument("--username", required=True)
user_auth_parser.add_argument("--password", required=True)


# create user parser

create_user_parser = auth_subparser.add_parser(
    name="create-user", help="Create a new user"
)

create_user_parser.add_argument("--username", required=True)


# password_parser = subparsers.add_parser("password", help="Password-related commands")
# password_subparser = password_parser.add_argument("--echo")
