from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


def create():
    global db
    db.create_all()


def initialize_database(application):
    global db
    db.init_app(application)
    # column = Column('name', String(100), primary_key=True)
    # add_column(db, 'table_name', column)
