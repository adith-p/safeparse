from rich import print
from rich.table import Table


def display_tables(values):
    table = Table()
    cols = [
        "password id",
        "login username",
        "login password",
        "note",
        "created at",
        "updated at",
    ]

    for col in cols:
        table.add_column(col)

    for val in values:
        table.add_row(*val, style="bold green")

    print(table)

def cipher_display_tables(values):
    table = Table()
    cols = [
        "password id",
        "login username",
        "login password",
        "note",
        "created at",
        "updated at",
    ]

    for col in cols:
        table.add_column(col)

    for val in values:
        row_data = list(val)
        original_password = str(row_data[2])
        row_data[2] = original_password[40:90]
        table.add_row(*row_data, style="bold green")
    print(table)


def display_tables_contact(values):
    table = Table()
    cols = [
        "contact id",
        "contact name",
        "contact email",
        "key fingerprint",
    ]

    for col in cols:
        table.add_column(col)
    for val in values:
        table.add_row(*val, style="bold green")

    print(table)
