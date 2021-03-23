from sqlalchemy import Column, Integer, ForeignKey, String, Time, Date, orm
from sqlalchemy_serializer import SerializerMixin

from Timary.data.db_session import SqlAlchemyBase


class Homework(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'homework'

    id = Column(Integer, ForeignKey('users.id'))
    homework_id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    lesson = Column(String)
    day_of_week = Column(String)
    num_of_week = Column(Integer)
    ready = Column(String)
    file = Column(String)

    user = orm.relation('User')