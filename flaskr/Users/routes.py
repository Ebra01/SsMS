from flask import Blueprint, jsonify, request, abort

from flask_login import current_user, logout_user
from flaskr.models.models import Users
from flaskr.Users.utils import addUserToDB, validate_current_user, deleteUser
from flaskr import login_manager, bcrypt

users = Blueprint('users', __name__)


@login_manager.user_loader
def load_user(user_id):
    """
    specify the current user, so we can use it in the frontend,
     and other endpoints.
    """
    return Users.query.get(int(user_id))


@users.route('/api/current_user')
def load_current():
    try:
        current = None
        if current_user.is_authenticated:
            current = current_user.display()

        return jsonify({
            'current_user': current,
            'success': True
        })
    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong in Our End!')


@users.route('/api/register', methods=['GET', 'POST'])
def register():

    # Check if there is a user logged-in already
    if current_user.is_authenticated:
        abort(400, 'You Are Logged-In Already, Logout to Register a New Account!')

    req = request.get_json()

    if not req:
        abort(400, 'Please Provide an Email and Password')

    email = req.get('email')
    password = req.get('password')

    if not email or not password:
        abort(400, 'Email, and Password Must be Filled!')

    body = {
        'email': email,
        'password': password,
        'type': 'user'
    }

    try:
        # Try to add user to Database
        addUserToDB(body)
    except Exception as e:
        print(e)
        abort(422, e)

    return jsonify({
        'user': 'User Was Registered Successfully!',
        'success': True
    })


@users.route('/api/login', methods=['GET', 'POST'])
def login():

    # Check if there is a user logged-in already
    if current_user.is_authenticated:
        abort(400, 'You Are Logged-In Already!')

    req = request.get_json()

    if not req:
        abort(400, 'Please Provide an Email and Password')

    email = req.get('email')
    password = req.get('password')

    try:
        # Try to log the user in as current user
        validate_current_user(email=email,
                              passw=password)
    except Exception as e:
        print(e)
        abort(422, e)

    return jsonify({
        'user': f'User "{email}" Logged-In Successfully!',
        'current_user': current_user.display(),
        'success': True
    })


@users.route('/api/logout')
def logout():
    # Check if Someone is logged-in
    if not current_user.is_authenticated:
        abort(400, 'You Are Not Logged-In!')

    # Try to logout user from login_manager
    try:
        logout_user()
    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong in Our End!')

    return jsonify({
        'user': 'User Logged out successfully!',
        'success': True
    })


@users.route('/api/users')
def get_users():
    return jsonify({
        'users': [u.display() for u in Users.query.all()],
        'success': True
    })


@users.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = Users.query.get(user_id)

    if not user:
        abort(404, f'No User Found with ID #{user_id}')

    user = user.display()

    return jsonify({
        'user': user,
        'success': True
    })


@users.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    user = Users.query.get(user_id)
    # Check if user exist, if not return 404
    if not user:
        abort(404, f'No User Found with ID #{user_id}')

    # try to delete user from database
    try:
        deleteUser(user.email)
        user_stat = f'User has been deleted successfully!'

    except Exception as e:
        print(e)
        user_stat = f'Couldn\'t delete User!'

    return jsonify({
        'user': user_stat,
        'succes': True
    })


@users.route('/api/users/<int:user_id>', methods=['PATCH'])
def update_users(user_id):
    user = Users.query.get(user_id)

    # Check if user exists
    if not user:
        abort(404, f'No User Found with ID #{user_id}')

    req = request.get_json()

    # Check if request is valid
    if not req:
        abort(400, 'Please Provide a New Password!')

    updated_password = req.get('password')

    try:
        if updated_password:
            hashed_password = bcrypt.generate_password_hash(updated_password)
            user.password = hashed_password

        user.update()

    except Exception as e:
        print(e)
        abort(500, e)

    return jsonify({
        'user': f'User #{user.email} has been updated!',
        'success': True
    })
