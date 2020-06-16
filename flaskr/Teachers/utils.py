from flaskr.models.models import Teachers


def checkTeachers(email):
    return Teachers.query.filter(Teachers.email == email).first()


def addTeacherToDB(body):

    phone = None

    try:
        full_name = body['full_name']
        age = body['age']
        email = body['email']
        school = body['school']
        grade = body['grade']
        print(grade)

        try:
            phone = body['phone']
        except KeyError:
            pass
    except KeyError:
        raise 422

    teacher = Teachers(
        full_name=full_name, age=age, email=email,
        phone=phone, school=school, grade=grade
    )
    teacher.insert()


