import datetime
from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    deadline: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

class Users(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    headman: Mapped[bool] = mapped_column(default=False)
    groupe: Mapped[str] = mapped_column(String(255), nullable=False)
    codeName: Mapped[str] = mapped_column(nullable=False)


class Subject(Base):
    __tablename__ = 'subject'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # requirements: Mapped['Post'] = mapped_column(nullable=True)
    # materials: Mapped['Post'] = mapped_column(nullable=True)
    requirements: Mapped['Post'] = relationship(backref='subject')
    materials: Mapped['Post'] = relationship(backref='subject')


class Semestr(Base):
    __tablename__ = 'semestr'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # subjects: Mapped[Subject] = mapped_column(Subject, nullable=True)
    # news: Mapped[Post] = mapped_column(Post, nullable=True)
    subjects: Mapped[Subject] = relationship(backref='semestr')
    news: Mapped[Post] = relationship(backref='semestr')


class Group(Base):
    __tablename__ = 'group'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    codeName: Mapped[int] = mapped_column(nullable=False)
    headmanID: Mapped[int] = mapped_column(nullable=False)
    # semesters: Mapped[Semestr] = mapped_column(Semestr, nullable=False)
    # notificationInterval: Mapped[int] = mapped_column(nullable=True) #в днях
    semesters: Mapped[Semestr] = relationship(backref='group')
    notificationInterval: Mapped[int] = relationship(backref='group') #в днях

