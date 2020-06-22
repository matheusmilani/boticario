from models import db
from models.user import UserModel
from sqlalchemy import create_engine


class Schema:
    @staticmethod
    def migration():
        db.configure_mappers()
        db.create_all()

    def prepare_db():
        from schema.seed import first_user, first_purchase
        first_user()
        return
