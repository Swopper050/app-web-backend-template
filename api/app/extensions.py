from flask_login import LoginManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class ModelBase(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=ModelBase)
api = Api()
login_manager = LoginManager()