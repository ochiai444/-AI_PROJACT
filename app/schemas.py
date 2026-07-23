from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class PlanRequest(BaseModel):
    subject: str
    exam_date: str
    study_time: int
    goal: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):

    messages: list

class ChatResponse(BaseModel):
    answer: str