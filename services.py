from flask import jsonify
from db import DatabaseProvider, SQLiteProvider
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @property
    def is_active(self):
        return True  # Adjust this based on your authentication logic

    @property
    def is_authenticated(self):
        return True  # Adjust this based on your authentication logic

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class WorkoutPlanBuilder:
    def __init__(self):
        self.workout_plan = {}

    def add_exercise(self, exercise, duration):
        self.workout_plan['exercise'] = exercise
        self.workout_plan['duration'] = duration

    def build(self):
        return self.workout_plan

class DatabaseAdapter:
    def __init__(self, database_provider):
        self.database_provider = database_provider

    def find_user_by_username(self, username):
        query = {"username": username}
        result = self.database_provider.get_data('users', query)
        return result[0] if result else None

    def save_user(self, username, hashed_password):
        data = {"username": username, "password": hashed_password}
        self.database_provider.save_data(data, "users")

    def get_data(self, table_name, params=None):
        return self.database_provider.get_data(table_name, params)

    def save_data(self, data, table_name):
        self.database_provider.save_data(data, table_name)

class UserObserver:
    def update(self, message):
        # Logic to notify users about achievements, progress, or reminders
        pass

def register_user(username, password, database_adapter):
    hashed_password = hash_password(password)

    existing_user = database_adapter.find_user_by_username(username)
    if existing_user:
        return {'message': 'Username already taken. Please choose another one.'}

    database_adapter.save_user(username, hashed_password)

    new_user_data = database_adapter.find_user_by_username(username)
    if new_user_data:
        new_user = User(id=new_user_data[0], username=new_user_data[1], password=new_user_data[2])
        return new_user

    return {'message': 'Failed to register user.'}

def login_user_service(username, password, database_adapter):
    hashed_password = hash_password(password)

    query = {"username": username, "password": hashed_password}
    result = database_adapter.get_data('users', query)
    if result:
        user_data = result[0]
        new_user = User(id=user_data[0], username=user_data[1], password=user_data[2])
        return new_user
    else:
        return None


def create_workout_plan(exercise, duration, database_adapter, user_observer):
    builder = WorkoutPlanBuilder()
    builder.add_exercise(exercise, duration)
    workout_plan = builder.build()

    database_adapter.save_data(workout_plan, table_name='workout_plans')

    user_observer.update('Congratulations! You have a new workout plan.')

    return jsonify({'message': 'Workout plan created successfully'})

def hash_password(password):
    # In a real-world scenario, use a secure hashing algorithm
    # For simplicity here, we'll just use a basic hash
    return hash(password)
