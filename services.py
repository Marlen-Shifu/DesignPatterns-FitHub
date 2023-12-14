from db import DatabaseProvider
from flask import jsonify


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

    def save_data(self, data):
        self.database_provider.save_data(data)

class UserObserver:
    def update(self, message):
        # Logic to notify users about achievements, progress, or reminders
        pass


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def register_user(username, password, users_database):
    if any(user.username == username for user in users_database):
        return jsonify({'message': 'Username already taken. Please choose another one.'}), 400

    new_user = User(username=username, password=password)
    users_database.append(new_user)

    return jsonify({'message': 'User registered successfully'})


def login_user(username, password, users_database):
    user = next((user for user in users_database if user.username == username and user.password == password), None)
    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


def create_workout_plan(exercise, duration, database_adapter, user_observer):
    builder = WorkoutPlanBuilder()
    builder.add_exercise(exercise, duration)
    workout_plan = builder.build()

    database_adapter.save_data(workout_plan)

    user_observer.update('Congratulations! You have a new workout plan.')

    return jsonify({'message': 'Workout plan created successfully'})
