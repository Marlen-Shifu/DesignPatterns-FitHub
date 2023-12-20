import sqlite3
from abc import ABC, abstractmethod

class DatabaseProvider(ABC):
    @abstractmethod
    def get_data(self, table_name, params=None):
        pass

    @abstractmethod
    def save_data(self, data, table_name):
        pass

class SQLiteProvider(DatabaseProvider):
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()  # Call the method to create tables

    def create_tables(self):
        # Create the necessary tables if they don't exist
        user_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        '''

        workout_table_query = '''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            exercise TEXT NOT NULL,
            duration INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        '''

        self.cursor.execute(user_table_query)
        self.cursor.execute(workout_table_query)
        self.connection.commit()

    def get_data(self, table_name, params=None):
        query = f"SELECT * FROM {table_name}"
        if params:
            query += " WHERE " + " AND ".join([f"{key} = ?" for key in params.keys()])
            result = self.cursor.execute(query, list(params.values()) if params else None).fetchall()
        else:
            result = self.cursor.execute(query).fetchall()
        return result

    def save_data(self, data, table_name):
        placeholders = ', '.join(['?'] * len(data))
        columns = ', '.join(data.keys())
        values = tuple(data.values())

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()

class MongoProvider(DatabaseProvider):
    # Implement MongoDB-specific database provider if needed
    pass
