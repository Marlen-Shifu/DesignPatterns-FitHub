from flask import Flask, request, jsonify
from db import SQLProvider, MongoProvider
from services import DatabaseAdapter, UserObserver, register_user, login_user, create_workout_plan, User

app = Flask(__name__)

users_database = []


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    return register_user(username, password, users_database)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    return login_user(username, password, users_database)


@app.route('/create_workout_plan', methods=['POST'])
def create_workout_plan_route():
    data = request.json
    exercise = data.get('exercise')
    duration = data.get('duration')

    sql_provider = SQLProvider(connection_string='your_sql_connection_string')
    mongo_provider = MongoProvider(connection_string='your_mongo_connection_string')
    database_adapter = DatabaseAdapter(database_provider=sql_provider)  # or mongo_provider

    user_observer = UserObserver()
    return create_workout_plan(exercise, duration, database_adapter, user_observer)


if __name__ == '__main__':
    app.run(debug=True)
