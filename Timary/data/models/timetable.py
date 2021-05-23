from sqlalchemy import Column, Integer, ForeignKey, String, Time, Date, orm
from sqlalchemy_serializer import SerializerMixin
from Timary.data.db_session import SqlAlchemyBase


class Timetable(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'timetable'

    lesson_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, ForeignKey('users.id'))
    lesson = Column(String)
    room = Column(String)
    day_of_week = Column(String)
    num_of_week = Column(String)
    time = Column(Time)

    user = orm.relation('User')