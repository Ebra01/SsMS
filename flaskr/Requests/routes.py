from flask import Blueprint, jsonify, abort, request
from flask_login import current_user
from flaskr.models.models import Requests
from flaskr.Requests.utils import execute_request
from flask_login import login_required
from datetime import datetime
import json

requests = Blueprint('requests', __name__)


# Create Requests :

@requests.route('/api/requests', methods=['POST'])
@login_required
def change_user_type():
    # Check if Someone is logged-in
    if not current_user.is_authenticated:
        pass
        # abort(400)

    req = request.get_json()

    if not req:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    request_type = 'CHANGE_USER_TYPE'
    full_name = req.get('full_name')
    age = req.get('age')
    phone = req.get('phone')
    switch_type = req.get('to_type')
    try:
        email = current_user.email
        type = current_user.type
        user_id = current_user.id
    except Exception as e:
        email = None
        type = None
        user_id = None
        print(e)
        abort(422, 'You Should Log-In First')

    request_body = {
                'full_name': full_name,
                'age': age,
                'email': email,
                'phone': phone,
                'type': type,
                'switchType': switch_type
            }
    try:
        # Create a new request
        request_ = Requests(
            user_id=user_id,
            request=json.dumps(request_body),
            request_type=request_type,
            date=datetime.now().strftime("%m-%d-%Y, %H:%M")
        )
        request_.insert()
    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    return jsonify({
        'request': 'Request has been created Successfully!',
        'success': True
    })


# End Create...

# Receive Requests :

@requests.route('/api/requests')
@login_required
def get_requests():
    requests_query = Requests.query.order_by('id').all()

    # Check if there is any requests
    if not requests_query:
        abort(404, 'No New Requests')

    requests_list = [r.display() for r in requests_query]

    return jsonify({
        'requests': requests_list,
        'success': True
    })


@requests.route('/api/requests/<int:request_id>')
@login_required
def get_request(request_id):

    request_ = Requests.query.get(request_id)

    if not request_:
        abort(404, f'No Request with ID#{request_id}')

    request_ = request_.display()

    return jsonify({
        'request': request_,
        'success': True
    })


@requests.route('/api/requests/<int:request_id>/review', methods=['PATCH'])
@login_required
def review_request(request_id):
    # This action is only accessable by a manager of the school itself.
    # if current_user and current_user.type == 'manager':

    request_ = Requests.query.get(request_id)

    if not request_:
        abort(404, f'No Request with ID#{request_id}')

    if request_.status == 'Closed':
        # Check if request is closed already.
        return jsonify({
            'request': f'Request #{request_id} is Closed!',
            'success': True
        })

    req = request.get_json()

    reason = req.get('reason') or 'None'
    status = req.get('status')
    completed = req.get('completed') or 'None'

    if not status:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    try:
        # Try to update the request
        request_.reasoning = reason
        request_.status = status
        request_.completed = completed

        request_.update()
    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    try:
        # Try to execute the request, if it's eligible
        if status == 'Accepted':
            execute_request(request_id)
        else:
            pass

    except Exception as e:
        print(e)
        abort(422, 'Cannot Execute The Request')

    request_view = request_.display()

    return jsonify({
        'request': f'Request #{request_id} has been updated!',
        'request_view': request_view,
        'success': True
    })


@requests.route('/api/requests/<int:request_id>', methods=['DELETE'])
@login_required
def delete_request(request_id):
    request_ = Requests.query.get(request_id)

    if not request_:
        abort(404, f'No Request with ID#{request_id}')

    try:
        # Try to delete a request
        request_.delete()
    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    return jsonify({
        'request': f'Request #{request_id} has been deleted Successfully!',
        'success': True
    })


# End Receive
