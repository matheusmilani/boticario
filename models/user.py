from datetime import datetime
from models import db
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), primary_key=False)
    cpf = db.Column(db.String(11), primary_key=False)
    email = db.Column(db.String(100), primary_key=False)
    password = db.Column(db.String(50), primary_key=False)
    recover_token = db.Column(db.String(255), primary_key=False)
    role = db.Column(db.Integer, primary_key=False)

    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    @staticmethod
    def get(id :int):
        return UserModel.query.filter_by(id=id).first()

    @staticmethod
    def get_by_email(email):
        return UserModel.query.filter_by(email=email).first()

    @staticmethod
    def get_by_cpf(cpf):
        return UserModel.query.filter_by(cpf=cpf).first()

    @staticmethod
    def list():
        return UserModel.query.all()

    @staticmethod
    def authenticate(email, password):
        user = UserModel.query.filter_by(email=email).first()
        if user:
            if sha256.verify(password, user.password):
                return user

        return None

    def save(self):
        self.password = sha256.hash('teste@1234')
        self.created_at = datetime.now()
        db.session.merge(self)
        db.session.commit()


    def update(self):
        if self.password and self.password.startswith(
                '$pbkdf2-sha256$') is False:
            self.password = sha256.hash(self.password)
        self.updated_at = datetime.now()
        db.session.merge(self)
        db.session.commit()

    @staticmethod
    def delete(id :int):
        UserModel.query.filter_by(id=id).delete()
        db.session.commit()
