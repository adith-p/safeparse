from pathlib import Path
import sqlite3


def does_db_exist():
    return Path("vault.db").exists()


def set_up_db():
    con = sqlite3.connect("vault.db")
    curr = con.cursor()
    return curr
