from flaskr.models.models import Students


def checkStudents(email):
    return Students.query.filter(Students.email == email).first()


def addStudentToDB(body):

    phone = None

    try:
        full_name = body['full_name']
        age = body['age']
        email = body['email']
        school = body['school']
        grade = body['grade']

        try:
            phone = body['phone']
        except KeyError:
            pass
    except KeyError:
        raise 422

    student = Students(
        full_name=full_name, age=age, email=email,
        phone=phone, school=school, grade=grade
    )
    student.insert()


