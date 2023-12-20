from flask import jsonify
from db import DatabaseProvider, SQLiteProvider
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class WorkoutPlanBuilder:
    def __init__(self):
        self.workout_plan = {}

    def add_exercise(self, exercise, duration):
        self.workout_plan['exercise'] = exercise
        self.workout_plan['duration'] = duration

    def build(self):
        return self.workout_plan

class DatabaseAdapter:
    def __init__(self, database_provider: DatabaseProvider):
        self.database_provider = database_provider

    def save_data(self, data, table_name):
        self.database_provider.save_data(data, table_name)

class UserObserver:
    def update(self, message):
        # Logic to notify users about achievements, progress, or reminders
        pass

def register_user(username, password, users_database, database_provider):
    if any(user.username == username for user in users_database):
        return jsonify({'message': 'Username already taken. Please choose another one.'}), 400

    # Hash the password before saving it to the database
    hashed_password = hash_password(password)

    new_user_id = len(users_database) + 1
    new_user = User(id=new_user_id, username=username, password=hashed_password)
    users_database.append(new_user)

    data = {'username': username, 'password': hashed_password}
    database_provider.save_data(data, table_name='users')

    return new_user

def login_user_service(username, password, database_provider):
    # Hash the entered password before checking against the stored hash
    hashed_password = hash_password(password)

    query = "SELECT * FROM users WHERE username=? AND password=?"
    result = database_provider.execute_query(query, (username, hashed_password))

    if result:
        # Return the User object for Flask-Login
        user_data = result[0]
        user = User(id=user_data[0], username=user_data[1], password=user_data[2])
        return user
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
