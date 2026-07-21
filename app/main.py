from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Base
from app.schemas import UserCreate, UserLogin, PlanRequest
from app.crud import create_user, get_user_by_username
from app.ai import generate_plan

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Study Planner"}


@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 이미 존재하는 회원인지 검증 로직을 추가하면 더 안전합니다.
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 아이디입니다."
        )
    
    create_user(db, user.username, user.password)
    return {"message": "회원가입 성공"}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="존재하지 않는 사용자입니다."
        )

    if db_user.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호가 일치하지 않습니다."
        )

    return {"message": "로그인 성공"}


@app.post("/generate-plan")
def create_plan(data: PlanRequest):
    result = generate_plan(
        data.subject,
        data.exam_date,
        data.study_time,
        data.goal
    )

    return {
        "plan": result
    }