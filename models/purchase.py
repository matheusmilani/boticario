from datetime import datetime
from models import db
from models.user import UserModel
from passlib.hash import pbkdf2_sha256 as sha256

class PurchaseModel(db.Model):
    __tablename__ = "purchase"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(255), primary_key=False)
    value = db.Column(db.Float, primary_key=False)
    id_reseller = db.Column(db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(50), primary_key=False, nullable=False)
    reseller = db.relationship(UserModel)

    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    @staticmethod
    def get(id :int):
        return PurchaseModel.query.filter_by(id=id).first()

    @staticmethod
    def get_by_reseller(id_reseller):
        return PurchaseModel.query.filter_by(id_reseller=id_reseller).all()

    @staticmethod
    def list():
        return PurchaseModel.query.all()

    def save(self):
        self.created_at = datetime.now()
        db.session.merge(self)
        db.session.commit()


    def update(self):
        self.updated_at = datetime.now()
        db.session.merge(self)
        db.session.commit()

    @staticmethod
    def delete(id :int):
        PurchaseModel.query.filter_by(id=id).delete()
        db.session.commit()
