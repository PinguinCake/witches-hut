import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class NameCompatibility(SqlAlchemyBase, UserMixin):
    __tablename__ = 'names'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    percent = sqlalchemy.Column(sqlalchemy.Integer)
    his_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    her_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'<Compatibility> For {self.his_name} and {self.her_name} is {self.percent}'
