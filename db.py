from abc import ABC, abstractmethod


class DatabaseProvider(ABC):
    @abstractmethod
    def save_data(self, data):
        pass


class SQLProvider(DatabaseProvider):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def save_data(self, data):
        # Logic to save data to SQL database using the connection_string
        pass


class MongoProvider(DatabaseProvider):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def save_data(self, data):
        # Logic to save data to MongoDB using the connection_string
        pass
