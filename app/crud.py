from sqlalchemy.orm import Session

from app.models import (
    User,
    StudyPlan,
    ChatHistory
)

from app.auth import hash_password



# ==========================
# 회원 관리
# ==========================

def get_user_by_username(
    db: Session,
    username: str
):

    return db.query(User)\
        .filter(User.username == username)\
        .first()



def create_user(
    db: Session,
    username: str,
    password: str
):

    user = User(
        username=username,
        password=hash_password(password)
    )


    db.add(user)

    db.commit()

    db.refresh(user)

    return user



# ==========================
# 공부 계획 저장
# ==========================

def save_plan(
    db: Session,
    username: str,
    subject: str,
    exam_date: str,
    study_time: int,
    goal: str,
    plan: str
):

    db_plan = StudyPlan(
        username=username,
        subject=subject,
        exam_date=exam_date,
        study_time=study_time,
        goal=goal,
        plan=plan
    )


    db.add(db_plan)

    db.commit()

    db.refresh(db_plan)

    return db_plan



# ==========================
# AI 채팅 저장
# ==========================

def save_chat(
    db: Session,
    username: str,
    role: str,
    content: str
):

    chat = ChatHistory(
        username=username,
        role=role,
        content=content
    )


    db.add(chat)

    db.commit()

    db.refresh(chat)

    return chat



# ==========================
# 내 공부 계획 조회
# ==========================

def get_user_plans(
    db: Session,
    username: str
):

    return db.query(StudyPlan)\
        .filter(
            StudyPlan.username == username
        )\
        .order_by(
            StudyPlan.created_at.desc()
        )\
        .all()



# ==========================
# 내 AI 대화 조회
# ==========================

def get_user_chats(
    db: Session,
    username: str
):

    return db.query(ChatHistory)\
        .filter(
            ChatHistory.username == username
        )\
        .order_by(
            ChatHistory.created_at
        )\
        .all()