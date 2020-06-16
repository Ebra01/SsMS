from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
import os


db = SQLAlchemy()


def app_config(app):
    # Setting up Database

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('PROJECT_SECRET')
    db.app = app
    db.init_app(app)
    # Setting up Migration
    Migrate(app, db)

    db.create_all()


# MODELS: TABLES

class Users(db.Model, UserMixin):
    """
    User's Table
    """
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    type = db.Column(db.String, nullable=False)

    def __init__(self, email, password, type):
        self.email = email
        self.password = password
        self.type = type

    def display(self):
        return {
            'id': self.id,
            'email': self.email,
            'type': self.type,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


class Requests(db.Model):
    """
    Requests Table
    """

    __tablename__ = 'Requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    request = db.Column(db.String(255), nullable=False)
    request_type = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)

    reasoning = db.Column(db.String, default='None')
    status = db.Column(db.String, default='open')
    completed = db.Column(db.String, default='None')

    def __init__(self, request, request_type, date, user_id):
        self.user_id = user_id
        self.request = request
        self.request_type = request_type
        self.date = date

    def display(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'request': self.request,
            'request_type': self.request_type,
            'date': self.date,
            'reason': self.reasoning,
            'status': self.status,
            'completed': self.completed
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


class Students(db.Model):
    """
    Students Table
    """

    __tablename__ = 'Students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True)
    full_name = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True)

    school_id = db.Column(db.Integer, db.ForeignKey('Schools.id'), nullable=False)
    school = db.relationship('Schools', backref='Students', lazy=True)

    grade_id = db.Column(db.Integer, db.ForeignKey('Classes.id'), nullable=False)
    grade = db.relationship('Classes', backref='Students', lazy=True)

    def __init__(self, full_name, age, email, phone, grade, school):
        self.full_name = full_name
        self.age = age
        self.email = email
        self.phone = phone
        self.grade = grade
        self.school = school

    def display(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'age': self.age,
            'email': self.email,
            'phone': self.phone,
            'school': self.school.shortDis(),
            'class': self.grade.shortDis()
        }

    def shortDis(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'age': self.age,
            'email': self.email,
            'phone': self.phone
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


class Teachers(db.Model):
    """
    Teachers Table
    """

    __tablename__ = 'Teachers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True)
    full_name = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True)

    school_id = db.Column(db.Integer, db.ForeignKey('Schools.id'), nullable=False)
    school = db.relationship('Schools', backref='Teachers', lazy=True)

    grade_id = db.Column(db.Integer, db.ForeignKey('Classes.id'), nullable=False)
    grade = db.relationship('Classes', backref='Teachers', lazy=True)

    def __init__(self, full_name, age, email, phone, grade, school):
        self.full_name = full_name
        self.age = age
        self.email = email
        self.phone = phone
        self.grade = grade
        self.school = school

    def display(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'age': self.age,
            'email': self.email,
            'phone': self.phone,
            'school': self.school.shortDis(),
            'class': self.grade.shortDis()
        }

    def shortDis(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'age': self.age,
            'email': self.email,
            'phone': self.phone
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


class Managers(db.Model):
    """
    Managers Table
    """

    __tablename__ = 'Managers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True)
    full_name = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True)

    school_id = db.Column(db.Integer, db.ForeignKey('Schools.id'), nullable=False)
    school = db.relationship('Schools', backref='Managers', lazy=True)

    def __init__(self, full_name, age, email, phone, school):
        self.full_name = full_name
        self.age = age
        self.email = email
        self.phone = phone
        self.school = school

    def display(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'age': self.age,
            'email': self.email,
            'phone': self.phone,
            'school': self.school.shortDis()
        }

    def shortDis(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'age': self.age,
            'email': self.email,
            'phone': self.phone
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


class Classes(db.Model):
    """
    Classes (Grades) Table
    """

    __tablename__ = 'Classes'

    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String, nullable=False)

    school_id = db.Column(db.Integer, db.ForeignKey('Schools.id'), nullable=False)
    school = db.relationship('Schools', backref='Classes', lazy=True)

    students = db.relationship('Students')

    teacher = db.relationship('Teachers')

    def __init__(self, grade, school):
        self.grade = grade
        self.school = school

    def display(self):

        return {
            'id': self.id,
            'class': self.grade,
            'school': self.school.shortDis(),
            'teacher': [t.shortDis() for t in self.teacher],
            'students': [s.shortDis() for s in self.students]
        }

    def shortDis(self):
        return {
            'id': self.id,
            'class': self.grade
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


class Schools(db.Model):
    """
    Schools Table
    """

    __tablename__ = 'Schools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)

    students = db.relationship('Students')
    teachers = db.relationship('Teachers')
    manager = db.relationship('Managers')
    classes = db.relationship('Classes')

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def display(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'classes': [c.shortDis() for c in self.classes],
            'students': [s.shortDis() for s in self.students],
            'teachers': [t.shortDis() for t in self.teachers],
            'manager': [m.shortDis() for m in self.manager]
        }

    def shortDis(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()
