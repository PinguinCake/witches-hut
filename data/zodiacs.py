import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class ZodiacCompatibility(SqlAlchemyBase, UserMixin):
    __tablename__ = 'zodiacs'

    percent = sqlalchemy.Column(sqlalchemy.Integer)
    his_sign = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    her_sign = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'<Compatibility> For {self.his_sign} and {self.her_sign} is {self.percent}'
