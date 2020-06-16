import string
from random import choice
from flaskr import bcrypt
from flaskr.models.models import Users
from flask_login import login_user


def createNonRegUser(email, type, iD):
    Password_Length = 16
    randomPass = string.ascii_letters + string.digits

    user_email = email
    password = ''.join((choice(randomPass) for _ in range(Password_Length)))
    user_type = type
    type_id = str(iD)

    # Adding the user to the Database
    try:
        body = {
            'email': user_email,
            'password': password,
            'type': user_type,
            'type_id': type_id
        }
        addUserToDB(body)
    except Exception as e:
        print(e)

    # Getting the user id
    user = Users.query.filter_by(email=email).one_or_none()

    return {
        'email': email,
        'type': type,
        'type_id': iD,
        'user_id': user.id
    }


def deleteUser(email):
    user = Users.query.filter(Users.email == email).first()

    # try to delete user from database
    try:
        user.delete()

    except Exception as e:
        print(e)


def addUserToDB(body):
    """
    Add users to the Database, by providing the body {email, password}
    and Register method {Def "Default", Non-Def "Registered manually"
    """
    registered_users = Users.query.all()
    registered_users = [u.display() for u in registered_users]
    registered_emails = [u['email'].lower() for u in registered_users]

    # Check if the email is not already in the Database, and
    # if not, adding the user credentials to the Database.
    if body['email'].lower() not in registered_emails:
        hashed_password = bcrypt.generate_password_hash(
            body['password']).decode('utf-8')

        new_user = Users(
            email=body['email'],
            password=hashed_password,
            type=body['type'],
        )
        new_user.insert()

        return True

    return Exception("User With Same Email is Already Registered!")


def validate_current_user(email, passw):
    user = Users.query.filter(Users.email.ilike(email)).first()

    # Check if entered password matches user's hashed password
    if user and bcrypt.check_password_hash(user.password, passw):
        # Logging the user as current user
        login_user(user)
    else:
        raise Exception("Wrong Credentials, Try Again!")

