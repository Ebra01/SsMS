from flaskr.models.models import Classes


def checkClasses():
    pass


def addClassToDB(body):

    try:
        grade = body['grade']
        school = body['school']

    except KeyError:
        raise 422

    class_ = Classes(
        grade=grade,
        school=school
    )
    class_.insert()
