import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class ZodiacCompatibility(SqlAlchemyBase, UserMixin):
    __tablename__ = 'zodiacs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    percent = sqlalchemy.Column(sqlalchemy.Integer)
    his_sign = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    her_sign = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return str(self.percent)
