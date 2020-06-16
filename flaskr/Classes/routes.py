from flask import Blueprint, abort, jsonify, request
from flaskr.models.models import Classes, Schools
from flaskr.Classes.utils import checkClasses, addClassToDB

classes = Blueprint('classes', __name__)


@classes.route('/api/classes')
def get_classes():
    classes_query = Classes.query.order_by('id').all()

    if not classes_query:
        abort(404, 'No Classes')

    classes_list = [c.display() for c in classes_query]

    return jsonify({
        'classes': classes_list,
        'success': True
    })


@classes.route('/api/classes/<int:class_id>')
def get_class(class_id):
    class_ = Classes.query.get(class_id)

    if not class_:
        abort(404, f'No Class with ID#{class_id}')

    class_ = class_.display()

    return jsonify({
        'class': class_,
        'success': True
    })


@classes.route('/api/classes', methods=['POST'])
def create_classes():

    req = request.get_json()

    # Check if request is valid
    if not req:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    grade = req.get('class')
    school_id = req.get('school')

    school = Schools.query.get(school_id)

    # Check if important data exists in request body
    if not grade or not school:
        abort(422, 'Fields Shouldn\'t Be Empty!')

    # Check if class already exist in the school
    if checkClasses():
        abort(400, f'A Class Is Already Registered In this School With: {grade}')

    body = {
        'grade': grade,
        'school': school
    }

    # Add class to the database
    try:
        addClassToDB(body)
    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    # return success value, and class info
    return jsonify({
        'class': f'Class "{grade}" was created successfully!',
        'success': True
    })


@classes.route('/api/classes/<int:class_id>', methods=['DELETE'])
def delete_classes(class_id):
    class_ = Classes.query.get(class_id)
    # Check if class exist, if not return 404
    if not class_:
        abort(404, f'No Class with ID#{class_id}')

    # try to delete class from database
    class_name = class_.grade
    try:
        class_.delete()

    except Exception as e:
        print(e)
        abort(500, 'Something Went Wrong In Our End.')

    return jsonify({
        'class': f'Class "{class_name}" has ben deleted!',
        'succes': True
    })


@classes.route('/api/classes/<int:class_id>', methods=['PATCH'])
def update_classes(class_id):
    class_ = Classes.query.get(class_id)

    # Check if class exists
    if not class_:
        abort(404, f'No Class with ID#{class_id}')

    req = request.get_json()

    # Check if request is valid
    if not req:
        abort(400, 'Fields Shouldn\'t Be Empty!')

    updated_grade = req.get('class')
    updated_school_id = req.get('school')

    try:
        if updated_grade:
            class_.grade = updated_grade
        else:
            raise Exception
        if updated_school_id:
            pass
            # updated_school = Schools.query.get(updated_school_id)
            # class_.school = updated_school

        class_.update()

    except Exception as e:
        print(e)
        abort(422, 'Cannot Update This Class.')

    return jsonify({
        'class': f'Class "{class_.grade}" has been updated!',
        'success': True
    })
