from flaskr.models.models import (Students, Teachers, Managers,
                                  Classes, Schools)
from sqlalchemy import func


def handleSearch(search, key):

    if key == 'all':
        results = searchForAll(search.lower())
    elif key == 'students':
        results = searchForStudents(search.lower())
    elif key == 'teachers':
        results = searchForTeachers(search.lower())
    elif key == 'managers':
        results = searchForManagers(search.lower())
    elif key == 'classes':
        results = searchForClasses(search.lower())
    elif key == 'schools':
        results = searchForSchools(search.lower())
    else:
        raise Exception(f'Wrong Search Key, Cannot Handle {key} !')

    return results


def searchForAll(search):
    return {
        'students': [u.display() for u in Students.query.filter(
            func.lower(Students.full_name).contains(search)
        ).all()],
        'teachers': [u.display() for u in Teachers.query.filter(
            func.lower(Teachers.full_name).contains(search)
        ).all()],
        'managers': [u.display() for u in Managers.query.filter(
            func.lower(Managers.full_name).contains(search)
        ).all()],
        'classes': [u.display() for u in Classes.query.filter(
            func.lower(Classes.grade).contains(search)
        ).all()],
        'schools': [u.display() for u in Schools.query.filter(
            func.lower(Schools.name).contains(search)
        ).all()]
    }


def searchForStudents(search):
    return {
        'students': [u.display() for u in Students.query.filter(
            func.lower(Students.full_name).contains(search)
        ).all()]
    }


def searchForTeachers(search):
    return {
        'teachers': [u.display() for u in Teachers.query.filter(
            func.lower(Teachers.full_name).contains(search)
        ).all()]
    }


def searchForManagers(search):
    return {
        'managers': [u.display() for u in Managers.query.filter(
            func.lower(Managers.full_name).contains(search)
        ).all()]
    }


def searchForClasses(search):
    return {
        'classes': [u.display() for u in Classes.query.filter(
            func.lower(Classes.grade).contains(search)
        ).all()]
    }


def searchForSchools(search):
    return {
        'schools': [u.display() for u in Schools.query.filter(
            func.lower(Schools.name).contains(search)
        ).all()]
    }
