from msr import db, login_manager
from msr import my_bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    repositories = db.relationship('Repository', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = my_bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return my_bcrypt.check_password_hash(self.password_hash, attempted_password)

class Repository(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    link = db.Column(db.String(length=1024), nullable=False, unique=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    analysis_date = db.Column(db.DateTime, nullable=True, default=None)
    analysed = db.Column(db.Integer(), nullable=True, default=0)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'Repository {self.name}'

class Users:
    def insert_user(self, user):
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(f'Error during insert user - {e}')

    def query_user_by_username(self, p_username):
        user = User.query.filter_by(username=p_username).first()
        return user
    def query_user_by_id(self, p_id):
        user = User.query.filter_by(id=p_id).first()
        return user
    
    def list_all_users(self):
        return User.query.all()

class Repositories:
    def insert_repository(self, repository):
        try:
            db.session.add(repository)
            db.session.commit()
        except Exception as e:
            print(f'Error during insert repository - {e}')

    def query_repository_by_name(self, p_name):
        repository = Repository.query.filter_by(name=p_name).first()
        return repository

    def query_repository_by_id(self, p_id):
        repository = Repository.query.filter_by(id=p_id).first()
        return repository
    
    def list_all_repositories(self):
        return Repository.query.all()

    def query_repositories_by_user_id(self, user_id):
        list_repositories = Repository.query.filter_by(owner=user_id).all()
        return list_repositories

    def update_repository_by_name(self, name, user_id, analysed):
        analysis_date = datetime.now()
        repository = Repository.query.filter_by(name=name, owner=user_id).first()
        repository.analysis_date = analysis_date
        repository.analysed = analysed
        db.session.add(repository)
        db.session.commit()

    def query_repositories_by_name_and_user_id(self, repository_name, user_id):
        list_repositories_by_user_id = Repository.query.filter_by(owner=user_id).all()
        list_repositories = []
        for each in list_repositories_by_user_id:
            if each.name == repository_name:
                list_repositories.append(each)

        return list_repositories