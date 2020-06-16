from flask import Blueprint, abort, jsonify, request
from flaskr.models.models import Schools
from flaskr.Schools.utils import checkSchools, addSchoolToDB
from flask_login import login_required

schools = Blueprint('schools', __name__)


@schools.route('/api/schools')
@login_required
def get_schools():
    schools_query = Schools.query.order_by('id').all()

    if not schools_query:
        abort(404, 'No Schools')

    schools_list = [s.display() for s in schools_query]

    return jsonify({
        'schools': schools_list,
        'success': True
    })


@schools.route('/api/schools/<int:school_id>')
@login_required
def get_school(school_id):
    school = Schools.query.get(school_id)

    if not school:
        abort(404, f'No School with ID#{school_id}')

    school = school.display()

    return jsonify({
        'school': school,
        'success': True
    })


@schools.route('/api/schools', methods=['POST'])
@login_required
def create_schools():
    req = request.get_json()

    # Check if request is valid
    if not req:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    name = req.get('name')
    email = req.get('email')

    # Check if important data exists in request body
    if not name or not email:
        abort(422, 'Fields Shouldn\'t Be Empty!')

    # Check if school already exist in the school
    if checkSchools(email):
        abort(400, f'A School Is Already Registered With: {email}')

    body = {
        'name': name,
        'email': email
    }

    # Add school to the database
    try:
        addSchoolToDB(body)
    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    # return success value, and school info
    return jsonify({
        'school': f'School "{name}" was created successfully!',
        'success': True
    })


@schools.route('/api/schools/<int:school_id>', methods=['DELETE'])
@login_required
def delete_schools(school_id):
    school = Schools.query.get(school_id)
    # Check if school exist, if not return 404
    if not school:
        abort(404, f'No School with ID#{school_id}')

    # try to delete school from database
    school_name = school.name
    try:
        school.delete()

    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    return jsonify({
        'school': f'School "{school_name}" has ben deleted!',
        'succes': True
    })


@schools.route('/api/schools/<int:school_id>', methods=['PATCH'])
@login_required
def update_schools(school_id):
    school = Schools.query.get(school_id)

    # Check if school exists
    if not school:
        abort(404, f'No School with ID#{school_id}')

    req = request.get_json()

    # Check if request is valid
    if not req:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    updated_name = req.get('name')

    try:
        if updated_name:
            school.name = updated_name

        school.update()

    except Exception as e:
        print(e)
        abort(422, 'Cannot Update This School.')

    return jsonify({
        'school': f'School "{school.name}" has been updated!',
        'success': True
    })
