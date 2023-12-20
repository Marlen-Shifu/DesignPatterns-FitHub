from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from db import SQLiteProvider
from services import DatabaseAdapter, UserObserver, register_user, login_user_service, create_workout_plan, User

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

users_database = []

# Instantiate SQLiteProvider once at the start of the application
sqlite_provider = SQLiteProvider(database_path='your_sqlite_database.db')

@login_manager.user_loader
def load_user(user_id):
    return next((user for user in users_database if user.id == int(user_id)), None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        user = login_user_service(username, password, sqlite_provider)
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid username or password')

    return render_template('login.html', message='')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_workout_plan', methods=['POST'])
@login_required
def create_workout_plan_route():
    data = request.json
    exercise = data.get('exercise')
    duration = data.get('duration')

    database_adapter = DatabaseAdapter(database_provider=sqlite_provider)
    user_observer = UserObserver()
    return create_workout_plan(exercise, duration, database_adapter, user_observer)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        database_adapter = DatabaseAdapter(database_provider=sqlite_provider)

        # Register user and log them in
        registered_user = register_user(username, password, users_database, database_adapter)
        login_user(registered_user)

        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/users')
def users():
    return render_template('users.html', users=users_database)

if __name__ == '__main__':
    app.run(debug=True)
