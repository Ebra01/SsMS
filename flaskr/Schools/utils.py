from flaskr.models.models import Schools


def checkSchools(email):

    return Schools.query.filter(Schools.email == email).first()


def addSchoolToDB(body):
    try:
        name = body['name']
        email = body['email']

    except KeyError:
        raise 422

    school = Schools(
        name=name,
        email=email
    )
    school.insert()
