import datetime
from sqlalchemy import DateTime, Float, String, Text, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Post(Base):
    __tablename__ = 'post'  

    text: Mapped[str] = mapped_column(Text, nullable=False)
    deadline: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    subject: Mapped['Subject'] = relationship(backref='post')
    material: Mapped['str'] = mapped_column(String(150), nullable=True)


class Subject(Base):
    __tablename__ = 'subject'

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    semestr_id: Mapped[int] = mapped_column(ForeignKey('semestr.id', ondelete='CASCADE'), nullable=False)
    semestr: Mapped['Semestr'] = relationship(backref='subject')


class Semestr(Base):
    __tablename__ = 'semestr'

    number: Mapped[int] = mapped_column(nullable=False)
    subjects: Mapped[Subject] = relationship(backref='semestr')
    group_id: Mapped[int] = mapped_column(ForeignKey('group.id', ondelete='CASCADE'), nullable=False)
    group: Mapped['Group'] = relationship(backref='semestr')


class Group(Base):
    __tablename__ = 'group'
    
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    codeName: Mapped[int] = mapped_column(nullable=False)
    headmanID: Mapped[int] = mapped_column(nullable=False)
    notificationInterval: Mapped[int] = mapped_column(nullable=True) #в днях

