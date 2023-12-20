from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from db import SQLiteProvider
from services import DatabaseAdapter, UserObserver, register_user, login_user_service, create_workout_plan, User

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

users_database = []

# Assuming you have a SQLite database named 'example.db'
database_provider = SQLiteProvider('example.db')
database_adapter = DatabaseAdapter(database_provider)

@login_manager.user_loader
def load_user(user_id):
    user_data = database_adapter.get_data('users', {'id': user_id})
    if user_data:
        user_data = user_data[0]
        return User(id=user_data[0], username=user_data[1], password=user_data[2])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        user = login_user_service(username, password, database_adapter)
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error_message='Invalid username or password')

    return render_template('login.html', error_message='')

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

    user_observer = UserObserver()
    return create_workout_plan(exercise, duration, database_adapter, user_observer)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        result = register_user(username, password, database_adapter)

        if isinstance(result, User):
            login_user(result)  # Auto-login the user after successful registration
            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        else:
            error_message = result['message']
            flash(error_message, 'error')

    return render_template('register.html', error_message=error_message)


@app.route('/users')
@login_required
def users():
    users_data = database_adapter.get_data('users')
    users_list = [{'id': user[0], 'username': user[1]} for user in users_data]
    return render_template('users.html', users=users_list)


if __name__ == '__main__':
    app.run(debug=True)
