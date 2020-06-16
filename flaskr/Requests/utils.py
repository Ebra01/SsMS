from flaskr.models.models import Requests, Users, Students, Teachers, Managers
from ast import literal_eval


def execute_request(request_id):
    request = Requests.query.get(request_id)

    if request.request_type == 'CHANGE_USER_TYPE':
        change_user_type(request.request)


def change_user_type(req):
    request = literal_eval(req)

    user = Users.query.filter_by(email=request['email']).first()
    user_id = user.id

    if user.type == request['type']:
        try:
            toType = request['switchType'].lower()
            user.type = toType
            user.update()

            create_personal(request, toType, user_id)
        except Exception as e:
            print(e)


def create_personal(req, toType, user_id):

    full_name = req['full_name']
    age = req['age']
    email = req['email']
    phone = req['phone']

    if toType == 'student':
        student = Students.query.filter_by(email=email).first()

        if not student:
            new_student = Students(
                full_name=full_name,
                age=age,
                email=email,
                phone=phone
            )
            new_student.user_id = user_id
            new_student.insert()

            # Change user type_id to student id
            student = Students.query.filter_by(email=email).first()
            user = Users.query.get(user_id)

            user.type_id = student.id
            user.update()

        else:
            student.full_name = full_name
            student.age = age
            student.phone = phone
            student.user_id = user_id

            student.update()

            # Change user type_id to student id
            user = Users.query.get(user_id)

            user.type_id = student.id
            user.update()

        teacher = Teachers.query.filter_by(email=email).first()

        if teacher:
            teacher.delete()

        manager = Managers.query.filter_by(email=email).first()

        if manager:
            manager.delete()

    if toType == 'teacher':
        teacher = Teachers.query.filter_by(email=email).first()

        if not teacher:
            new_teacher = Teachers(
                full_name=full_name,
                age=age,
                email=email,
                phone=phone
            )
            new_teacher.user_id = user_id
            new_teacher.insert()

            # Change user type_id to teacher id
            teacher = Teachers.query.filter_by(email=email).first()
            user = Users.query.get(user_id)

            user.type_id = teacher.id
            user.update()

        else:
            teacher.full_name = full_name
            teacher.age = age
            teacher.phone = phone
            teacher.user_id = user_id

            teacher.update()

            # Change user type_id to teacher id
            user = Users.query.get(user_id)

            user.type_id = teacher.id
            user.update()

        student = Students.query.filter_by(email=email).first()

        if student:
            student.delete()

        manager = Managers.query.filter_by(email=email).first()

        if manager:
            manager.delete()

    if toType == 'manager':
        manager = Managers.query.filter_by(email=email).first()

        if not manager:
            new_manager = Managers(
                full_name=full_name,
                age=age,
                email=email,
                phone=phone
            )
            new_manager.user_id = user_id
            new_manager.insert()

            # Change user type_id to manager id
            manager = Managers.query.filter_by(email=email).first()
            user = Users.query.get(user_id)

            user.type_id = manager.id
            user.update()

        else:
            manager.full_name = full_name
            manager.age = age
            manager.phone = phone
            manager.user_id = user_id

            manager.update()

            # Change user type_id to manager id
            user = Users.query.get(user_id)

            user.type_id = manager.id
            user.update()

        student = Students.query.filter_by(email=email).first()

        if student:
            student.delete()

        teahcer = Teachers.query.filter_by(email=email).first()

        if teahcer:
            teahcer.delete()
