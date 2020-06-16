from flask import Blueprint, abort, jsonify, request
from flaskr.models.models import Managers, Schools
from flaskr.Managers.utils import checkManagers, addManagerToDB
from flaskr.Users.utils import createNonRegUser, deleteUser
from flask_login import login_required

managers = Blueprint('managers', __name__)


@managers.route('/api/managers')
@login_required
def get_managers():
    managers_query = Managers.query.order_by('id').all()

    if not managers_query:
        abort(404, 'No Managers')

    managers_list = [m.display() for m in managers_query]

    return jsonify({
        'managers': managers_list,
        'success': True
    })


@managers.route('/api/managers/<int:manager_id>')
@login_required
def get_manager(manager_id):
    manager = Managers.query.get(manager_id)

    if not manager:
        abort(404, f'No Manager with ID#{manager_id}')

    manager = manager.display()

    return jsonify({
        'manager': manager,
        'success': True
    })


@managers.route('/api/managers', methods=['POST'])
@login_required
def create_managers():

    req = request.get_json()

    # Check if request is valid
    if not req:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    full_name = req.get('full_name')
    age = req.get('age')
    email = req.get('email')
    phone = req.get('phone')
    school_id = req.get('school')

    school = Schools.query.get(school_id)

    # Check if important data exists in request body
    if not full_name or not age or not email or not school:
        abort(422, 'Fields Shouldn\'t Be Empty!')

    # Check if email already registered in database
    if checkManagers(email):
        abort(400, f'A Manager Is Already Registered With: {email}')

    body = {
        'full_name': full_name,
        'age': age,
        'email': email,
        'phone': phone,
        'school': school
    }

    # Add manager to the database
    try:
        addManagerToDB(body)
    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    manager = Managers.query.filter_by(email=email).one_or_none()
    user_id = None

    # Create A new User.
    try:
        type = 'manager'
        user_info = createNonRegUser(email, type, manager.id)
        user = {
            'user_email': user_info['email'],
            'user_type': user_info['type'],
            'manager_id': user_info['type_id']
        }

        # Try to get the user_id
        try:
            user_id = user_info['user_id']
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
        user = None

    # Update user_id in manager.
    try:
        manager.user_id = user_id
        manager.update()
    except Exception as e:
        print(e)

    # return success value, and manager info
    return jsonify({
        'manager': f'Manager "{full_name}" was created successfully!',
        'user': user,
        'success': True
    })


@managers.route('/api/managers/<int:manager_id>', methods=['DELETE'])
@login_required
def delete_managers(manager_id):
    manager = Managers.query.get(manager_id)
    # Check if manager exist, if not return 404
    if not manager:
        abort(404, f'No Manager with ID#{manager_id}')

    # try to delete manager from database
    manager_name = manager.full_name
    user_stat = None
    try:

        # try to delete the manager user for database
        try:
            deleteUser(manager.email)
            user_stat = f'Manager #{manager_id} User has been deleted successfully!'
        except Exception as e:
            user_stat = f'Couldn\'t delete Manager #{manager_id} User!'
            print(e)

        manager.delete()

    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    return jsonify({
        'manager': f'Manager "{manager_name}" has ben deleted!',
        'user': user_stat,
        'succes': True
    })


@managers.route('/api/managers/<int:manager_id>', methods=['PATCH'])
@login_required
def update_managers(manager_id):
    manager = Managers.query.get(manager_id)

    # Check if manager exists
    if not manager:
        abort(404, f'No Manager with ID#{manager_id}')

    req = request.get_json()

    # Check if request is valid
    if not req:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    updated_full_name = req.get('full_name')
    updated_age = req.get('age')
    updated_phone = req.get('phone')
    updated_school_id = req.get('school')

    updated_school = Schools.query.get(updated_school_id)

    try:
        if updated_full_name:
            manager.full_name = updated_full_name
        if updated_age:
            manager.age = updated_age
        if updated_phone:
            manager.phone = updated_phone
        if updated_school:
            manager.school = updated_school

        manager.update()

    except Exception as e:
        print(e)
        abort(422, 'Cannot Update This Manager.')

    return jsonify({
        'manager': f'Manager "{manager.full_name}" has ben deleted!',
        'success': True
    })

