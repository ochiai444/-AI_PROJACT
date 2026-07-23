from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database import Base



# 사용자
class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True
    )


    username = Column(
        String,
        unique=True
    )


    password = Column(
        String
    )




# 공부 계획 저장
class StudyPlan(Base):

    __tablename__ = "study_plans"


    id = Column(
        Integer,
        primary_key=True
    )


    username = Column(
        String
    )


    subject = Column(
        String
    )


    exam_date = Column(
        String
    )


    study_time = Column(
        Integer
    )


    goal = Column(
        String
    )


    plan = Column(
        Text
    )


    created_at = Column(
        DateTime,
        default=datetime.now
    )




# AI 채팅 저장
class ChatHistory(Base):

    __tablename__ = "chat_history"


    id = Column(
        Integer,
        primary_key=True
    )


    username = Column(
        String
    )


    role = Column(
        String
    )


    content = Column(
        Text
    )


    created_at = Column(
        DateTime,
        default=datetime.now
    )