from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str

    class PlanRequest(BaseModel):
    subject: str
    exam_date: str
    study_time: str
    goal: str