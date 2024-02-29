from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)

socketio = SocketIO(app)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "/"

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

@app.route('/test')
def test():
    print(current_user.id)
    print(current_user.name)
    print(current_user.username)
    return json.dumps({
        'id': current_user.id,
        'name': current_user.name,
        'username': current_user.username
    })

@app.route('/')
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('indexFunc'))
    return render_template('login.html')


@app.route('/createAccountPage')
def create_account_page():
    return render_template('createAccount.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return jsonify({'success': True, 'message':f'Logged in as {username}'})
            else:
                return jsonify({'success': False, 'message':'Incorrect Password'})
        else:
            return jsonify({'success': False, 'message':'Username not found!'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

@app.route('/createAccount', methods=['POST'])
def create_account():
    try:
        data = request.get_json()
        # Extract data from the JSON body
        name = data.get('name')
        username = data.get('username')
        password = data.get('password')

        if not name or not username or not password:
            return jsonify({'success': False, 'error': 'Missing required fields'})
        # Check if the username is already taken
        existingUserUsername = User.query.filter_by(
            username=username
        ).first()
        if existingUserUsername:
            return jsonify({'success': False, 'error': 'Username already taken'})
        # Add the user to the global variable (replace this with database storage)
        hashedPassword = bcrypt.generate_password_hash(password=password)
        newUser = User(name=name, username=username, password=hashedPassword)
        db.session.add(newUser)
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/index')
@login_required
def indexFunc():
    name = current_user.name
    if name:
        return render_template('index.html', name=name)
    else:
        return 'Unauthorized', 401

@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    
    # Broadcast the message to all clients
    emit('receive_message', {'message': message}, broadcast=True)

if __name__ == '__main__':
    # Use eventlet as the web server to support WebSocket

    socketio.run(app, debug=True, host='0.0.0.0', port=8000)



