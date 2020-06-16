from flask import Blueprint, abort, jsonify, request
from flaskr.models.models import Students, Schools, Classes
from flaskr.Students.utils import checkStudents, addStudentToDB
from flaskr.Users.utils import createNonRegUser, deleteUser
from flask_login import login_required

students = Blueprint('students', __name__)


@students.route('/api/students')
@login_required
def get_students():
    students_query = Students.query.order_by('id').all()

    if not students_query:
        abort(404, 'No Students')

    students_list = [s.display() for s in students_query]

    return jsonify({
        'students': students_list,
        'success': True
    })


@students.route('/api/students/<int:student_id>')
@login_required
def get_student(student_id):
    student = Students.query.get(student_id)

    if not student:
        abort(404, f'No Student with ID#{student_id}')

    student = student.display()

    return jsonify({
        'student': student,
        'success': True
    })


@students.route('/api/students', methods=['POST'])
@login_required
def create_students():

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
    if checkStudents(email):
        abort(400, f'A Student Is Already Registered With: {email}')

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

    # Add student to the database
    try:
        addStudentToDB(body)
    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    student = Students.query.filter_by(email=email).one_or_none()
    user_id = None

    # Create A new User.
    try:
        type = 'student'
        user_info = createNonRegUser(email, type, student.id)
        user = {
            'user_email': user_info['email'],
            'user_type': user_info['type'],
            'student_id': user_info['type_id']
        }

        # Try to get the user_id
        try:
            user_id = user_info['user_id']
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
        user = None

    # Update user_id in student.
    try:
        student.user_id = user_id
        student.update()
    except Exception as e:
        print(e)

    # return success value, and student info
    return jsonify({
        'student': f'Student "{full_name}" was created successfully!',
        'user': user,
        'success': True
    })


@students.route('/api/students/<int:student_id>', methods=['DELETE'])
@login_required
def delete_students(student_id):
    student = Students.query.get(student_id)
    # Check if student exist, if not return 404
    if not student:
        abort(404, f'No Student with ID#{student_id}')

    # try to delete student from database
    student_name = student.full_name
    user_stat = None
    try:

        # try to delete the student user for database
        try:
            deleteUser(student.email)
            user_stat = f'Student "{student_name}" User has been deleted successfully!'
        except Exception as e:
            user_stat = f'Couldn\'t delete Student "{student_name}" User!'
            print(e)

        student.delete()

    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    return jsonify({
        'student': f'Student "{student_name}" has ben deleted!',
        'user': user_stat,
        'succes': True
    })


@students.route('/api/students/<int:student_id>', methods=['PATCH'])
@login_required
def update_students(student_id):
    student = Students.query.get(student_id)

    # Check if student exists
    if not student:
        abort(404, f'No Student with ID#{student_id}')

    req = request.get_json()

    # Check if request is valid
    if not req:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    updated_full_name = req.get('full_name')
    updated_age = req.get('age')
    updated_phone = req.get('phone')

    try:
        if updated_full_name:
            student.full_name = updated_full_name
        if updated_age:
            student.age = updated_age
        if updated_phone:
            student.phone = updated_phone

        student.update()

    except Exception as e:
        print(e)
        abort(422, 'Cannot Update This Student.')

    return jsonify({
        'student': f'Student "{student.full_name}" has been updated!',
        'success': True
    })

