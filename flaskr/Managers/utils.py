from flaskr.models.models import Managers


def checkManagers(email):
    return Managers.query.filter(Managers.email == email).first()


def addManagerToDB(body):

    phone = None

    try:
        full_name = body['full_name']
        age = body['age']
        email = body['email']
        school = body['school']

        try:
            phone = body['phone']
        except KeyError:
            pass
    except KeyError:
        raise 422

    manager = Managers(
        full_name=full_name, age=age, email=email, phone=phone, school=school
    )
    manager.insert()


