import os
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from app.schemas import (
    UserCreate,
    PlanRequest,
    ChatRequest
)

from app.database import engine, get_db
from app.models import Base,StudyPlan
from app.crud import (
    create_user,
    get_user_by_username,
    save_plan,
    save_chat,
    get_user_plans,
    get_user_chats
)
from app.ai import generate_plan, chat
from app.auth import verify_password, create_token, decode_token



# ======================
# DB 생성
# ======================

Base.metadata.create_all(bind=engine)



# ======================
# FastAPI 설정
# ======================

app = FastAPI(
    title="AI Study Planner"
)



# ======================
# HTML / Static 설정
# ======================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


templates = Jinja2Templates(
    directory=os.path.join(
        BASE_DIR,
        "templates"
    )
)


app.mount(
    "/static",
    StaticFiles(
        directory=os.path.join(
            BASE_DIR,
            "static"
        )
    ),
    name="static"
)



# ======================
# JWT 설정
# ======================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)



def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    payload = decode_token(token)


    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다."
        )


    username = payload.get("sub")


    if username is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자 정보가 없습니다."
        )


    return username



# ======================
# 페이지 이동
# ======================


@app.get("/")
def home():

    return {
        "message":"AI Study Planner"
    }



@app.get("/web")
def web(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )



@app.get("/planner")
def planner(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="planner.html",
        context={}
    )



@app.get("/login-page")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )



@app.get("/signup-page")
def signup_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={}
    )
@app.get("/mypage")
def mypage(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="mypage.html",
        context={}
    )


# ======================
# 회원가입
# ======================


@app.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_username(
        db,
        user.username
    )


    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 아이디입니다."
        )


    create_user(
        db,
        user.username,
        user.password
    )


    return {
        "message":"회원가입 성공"
    }



# ======================
# 로그인
# ======================


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):


    db_user = get_user_by_username(
        db,
        form_data.username
    )


    if db_user is None:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="존재하지 않는 사용자입니다."
        )



    if not verify_password(
        form_data.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호가 일치하지 않습니다."
        )



    token = create_token(
        form_data.username
    )



    return {

        "message":"로그인 성공",

        "access_token":token,

        "token_type":"bearer"

    }



# ======================
# AI 공부 계획 생성
# ======================


@app.post("/generate-plan")
def create_plan(
    data: PlanRequest,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):


    result = generate_plan(
        data.subject,
        data.exam_date,
        data.study_time,
        data.goal
    )


    # 공부 계획 DB 저장
    save_plan(
        db,
        username,
        data.subject,
        data.exam_date,
        data.study_time,
        data.goal,
        result
    )


    return {

        "username": username,

        "message": "공부 계획 생성 완료",

        "plan": result

    }



# ======================
# AI 채팅
# ======================


@app.post("/chat")
def chat_api(
    data: ChatRequest,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):

    print("사용자 메시지:", data.messages)


    messages = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in data.messages
    ]


    answer = chat(messages)


    # 사용자 질문 저장
    for msg in messages:

        if msg["role"] == "user":

            save_chat(
                db,
                username,
                "user",
                msg["content"]
            )


    # AI 답변 저장
    save_chat(
        db,
        username,
        "assistant",
        answer
    )


    print("AI 답변:", answer)


    return {
        "answer": answer
    }

@app.get("/my-plans")
def my_plans(
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):

    plans = get_user_plans(
        db,
        username
    )


    return [
        {
            "id": p.id,
            "subject": p.subject,
            "exam_date": p.exam_date,
            "study_time": p.study_time,
            "goal": p.goal,
            "plan": p.plan,
            "created_at": p.created_at
        }
        for p in plans
    ]



@app.get("/my-chats")
def my_chats(
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):

    chats = get_user_chats(
        db,
        username
    )


    return [
        {
            "id": c.id,
            "role": c.role,
            "content": c.content,
            "created_at": c.created_at
        }
        for c in chats
    ]

# ======================
# PDF 다운로드
# ======================

@app.get("/download-plan/{plan_id}")
def download_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):

    plan = db.query(StudyPlan).filter(
        StudyPlan.id == plan_id,
        StudyPlan.username == username
    ).first()


    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="계획을 찾을 수 없습니다."
        )


    filename = f"study_plan_{plan_id}.pdf"


    pdf_dir = "pdf"

    os.makedirs(
        pdf_dir,
        exist_ok=True
    )


    pdf_path = os.path.join(
        pdf_dir,
        filename
    )


    pdfmetrics.registerFont(
        UnicodeCIDFont(
            "HYSMyeongJo-Medium"
        )
    )


    c = canvas.Canvas(
        pdf_path,
        pagesize=A4
    )


    width, height = A4

    y = height - 50


    c.setFont(
        "HYSMyeongJo-Medium",
        14
    )


    c.drawString(
        50,
        y,
        "AI Study Planner"
    )


    y -= 40


    c.setFont(
        "HYSMyeongJo-Medium",
        11
    )


    contents = [

        f"과목 : {plan.subject}",

        f"시험일 : {plan.exam_date}",

        f"공부 시간 : {plan.study_time}시간",

        f"목표 : {plan.goal}",

        "",

        "AI 추천 계획",

        plan.plan

    ]


    for text in contents:

        for line in text.split("\n"):


            if y < 50:

                c.showPage()

                c.setFont(
                    "HYSMyeongJo-Medium",
                    11
                )

                y = height - 50


            c.drawString(
                50,
                y,
                line
            )


            y -= 20



    c.save()


    return FileResponse(

        pdf_path,

        media_type="application/pdf",

        filename=filename

    )