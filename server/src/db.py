import os

import psycopg2
from dotenv import load_dotenv

load_dotenv("./.env")


class DB:
    _instance = None

    def __init__(self):
        self._connection = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PSWD"),
            database=os.environ.get("DB_DBNAME"),
        )

        self.run_migrations()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DB()
        return cls._instance

    @staticmethod
    def row_to_dict(r):
        return {
            "id": r[0],
            "body": r[1],
            "done": r[2],
            "created_at": r[3].isoformat(),
        }

    def run_migrations(self):
        try:
            cursor = self._connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS todos(
                    id SERIAL PRIMARY KEY, 
                    body TEXT NOT NULL,
                    done BOOLEAN NOT NULL, 
                    created_at timestamp NOT NULL DEFAULT NOW()
                );"""

            cursor.execute(query)
            self._connection.commit()
        except Exception:
            self._connection.rollback()

    def insert_todo(self, body: str, done: bool):
        try:
            cursor = self._connection.cursor()
            query = "INSERT INTO todos (body, done) VALUES(%s, %s) RETURNING *;"
            cursor.execute(query, [body, done])
            self._connection.commit()
            return DB.row_to_dict(cursor.fetchone())

        except Exception:
            self._connection.rollback()
            return None

    def fetch_todo_by_id(self, id: int):
        cursor = self._connection.cursor()
        query = "SELECT * FROM todos where id=%s LIMIT 1;"
        cursor.execute(query, [id])
        return DB.row_to_dict(cursor.fetchone())

    def fetch_all_todos(self):
        cursor = self._connection.cursor()
        query = "SELECT * FROM todos;"
        cursor.execute(query)
        return list(map(DB.row_to_dict, cursor.fetchall()))

    def toggle_todo(self, id: int):
        try:
            cursor = self._connection.cursor()
            query = "UPDATE todos SET done = NOT done WHERE id=%s RETURNING *;"
            cursor.execute(query, [id])
            self._connection.commit()
            return DB.row_to_dict(cursor.fetchone())

        except Exception:
            self._connection.rollback()
            return None

    def delete_todo_by_id(self, id: int):
        try:
            cursor = self._connection.cursor()
            query = "DELETE FROM todos WHERE id=%s"
            cursor.execute(query, [id])
            self._connection.commit()
            return True
        except Exception:
            self._connection.rollback()
            return False
