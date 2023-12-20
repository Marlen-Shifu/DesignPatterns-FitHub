import sqlite3
from abc import ABC, abstractmethod

class DatabaseProvider(ABC):
    @abstractmethod
    def save_data(self, data, table_name):
        pass

    @abstractmethod
    def execute_query(self, query, parameters):
        pass

class SQLiteProvider(DatabaseProvider):
    def __init__(self, database_path):
        self.database_path = database_path

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS workout_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exercise TEXT NOT NULL,
                    duration INTEGER NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

    def save_data(self, data, table_name):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()

        placeholders = ', '.join(['?'] * len(data))
        columns = ', '.join(data.keys())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(data.values()))

        connection.commit()
        connection.close()

    def execute_query(self, query, parameters):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()

        cursor.execute(query, parameters)
        result = cursor.fetchall()

        connection.close()
        return result
