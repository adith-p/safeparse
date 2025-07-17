from pathlib import Path
import sqlite3

from sqlite3 import Cursor


class Database_controller:
    def __init__(self):
        self.db_name = "vault.db"

    # def _execute_query(self, curr, sql_query):
    #     try:
    #         result = curr.execute(sql_query)
    #     except Exception as e:
    #         raise e
    #     finally:
    #         curr.close()

    #     return result

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_user(self, username: str, hashed_password: str, hash_salt: str):
        sql_query = """
            INSERT INTO users(username, master_password_hash, master_password_salt)
            VALUES (?, ?, ?);
            """
        conn = self.get_connection()
        curr = conn.cursor()
        try:
            curr.execute(sql_query, (username, hashed_password, hash_salt))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()
        # self._execute_query(curr, sql_query)

    def get_user(self, username: str) -> Cursor:
        sql_query = "SELECT * from users WHERE username = (?);"

        conn = self.get_connection()
        curr = conn.cursor()
        try:
            result = curr.execute(sql_query, (username,))

            return result.fetchone()
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()
