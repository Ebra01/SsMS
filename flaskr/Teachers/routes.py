from flask import Blueprint, abort, jsonify, request
from flaskr.models.models import Teachers, Schools, Classes
from flaskr.Teachers.utils import checkTeachers, addTeacherToDB
from flaskr.Users.utils import createNonRegUser, deleteUser
from flask_login import login_required

teachers = Blueprint('teachers', __name__)


@teachers.route('/api/teachers')
@login_required
def get_teachers():
    teachers_query = Teachers.query.order_by('id').all()

    if not teachers_query:
        abort(404, 'No Teachers')

    teachers_list = [t.display() for t in teachers_query]

    return jsonify({
        'teachers': teachers_list,
        'success': True
    })


@teachers.route('/api/teachers/<int:teacher_id>')
@login_required
def get_teacher(teacher_id):
    teacher = Teachers.query.get(teacher_id)

    if not teacher:
        abort(404, f'No Teacher with ID#{teacher_id}')

    teacher = teacher.display()

    return jsonify({
        'teacher': teacher,
        'success': True
    })


@teachers.route('/api/teachers', methods=['POST'])
@login_required
def create_teachers():

    req = request.get_json()

    # Check if request is valid
    if not req:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    full_name = req.get('full_name')
    age = req.get('age')
    email = req.get('email')
    phone = req.get('phone')
    school_id = req.get('school')
    grade_id = req.get('class')

    # Check if important data exists in request body
    if not full_name or not age or not email or not school_id or not grade_id:
        abort(422, 'Fields Shouldn\'t Be Empty!')

    # Check if email already registered in database
    if checkTeachers(email):
        abort(400, f'A Teacher Is Already Registered With: {email}')

    school = Schools.query.get(school_id)
    grade = Classes.query.get(grade_id)

    body = {
        'full_name': full_name,
        'age': age,
        'email': email,
        'phone': phone,
        'school': school,
        'grade': grade
    }

    # Add teacher to the database
    try:
        addTeacherToDB(body)
    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    teacher = Teachers.query.filter_by(email=email).one_or_none()
    user_id = None

    # Create A new User.
    try:
        type = 'teacher'
        user_info = createNonRegUser(email, type, teacher.id)
        user = {
            'user_email': user_info['email'],
            'user_type': user_info['type'],
            'teacher_id': user_info['type_id']
        }

        # Try to get the user_id
        try:
            user_id = user_info['user_id']
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
        user = None

    # Update user_id in teacher.
    try:
        teacher.user_id = user_id
        teacher.update()
    except Exception as e:
        print(e)

    # return success value, and teacher info
    return jsonify({
        'teacher': f'Teacher "{full_name}" was created successfully!',
        'user': user,
        'success': True
    })


@teachers.route('/api/teachers/<int:teacher_id>', methods=['DELETE'])
@login_required
def delete_teachers(teacher_id):
    teacher = Teachers.query.get(teacher_id)
    # Check if teacher exist, if not return 404
    if not teacher:
        abort(404, f'No Teacher with ID#{teacher_id}')

    # try to delete teacher from database
    teacher_name = teacher.full_name
    user_stat = None
    try:

        # try to delete the teacher user for database
        try:
            deleteUser(teacher.email)
            user_stat = f'Teacher #{teacher_id} User has been deleted successfully!'
        except Exception as e:
            user_stat = f'Couldn\'t delete Teacher #{teacher_id} User!'
            print(e)

        teacher.delete()

    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    return jsonify({
        'teacher': f'Teacher "{teacher_name}" has ben deleted!',
        'user': user_stat,
        'succes': True
    })


@teachers.route('/api/teachers/<int:teacher_id>', methods=['PATCH'])
@login_required
def update_teachers(teacher_id):
    teacher = Teachers.query.get(teacher_id)

    # Check if teacher exists
    if not teacher:
        abort(404, f'No Teacher with ID#{teacher_id}')

    req = request.get_json()

    # Check if request is valid
    if not req:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    updated_full_name = req.get('full_name')
    updated_age = req.get('age')
    updated_phone = req.get('phone')

    try:
        if updated_full_name:
            teacher.full_name = updated_full_name
        if updated_age:
            teacher.age = updated_age
        if updated_phone:
            teacher.phone = updated_phone

        teacher.update()

    except Exception as e:
        print(e)
        abort(422, 'Cannot Update This Teacher.')

    return jsonify({
        'teacher': f'Teacher "{teacher.full_name}" has ben deleted!',
        'success': True
    })

