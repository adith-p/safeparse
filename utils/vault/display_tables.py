from rich.table import Table
from rich import print


def display_tables(values):
    table = Table()
    cols = ['login username', 'login password', 'note','created at','updated at']

    for col in cols:
        table.add_column(col)
    for val in values:
        table.add_row(*val, style="bold green")

    print(table)


