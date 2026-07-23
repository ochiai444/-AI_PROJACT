import os
import requests
from dotenv import load_dotenv

load_dotenv()

# ======================
# ML API 설정
# ======================
BASE_URL = (os.getenv("MLAPI_BASE_URL") or "").rstrip("/")
MLAPI_URL = BASE_URL + "/chat/completions"

API_KEY = os.getenv("ELICE_API_KEY")
MODEL = os.getenv("MLAPI_MODEL")

print("BASE URL:", MLAPI_URL)
print("MODEL:", MODEL)


# ======================
# 공부 계획 생성
# ======================
def generate_plan(subject, exam_date, study_time, goal):
    prompt = f"""
과목: {subject}
시험일: {exam_date}
하루 공부 가능 시간: {study_time}
목표: {goal}

위 정보를 바탕으로 날짜별 학습 계획을 작성해줘.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "너는 학습 계획을 전문적으로 작성하는 AI 스터디 플래너이다."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(
        MLAPI_URL,
        json=payload,
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    if response.status_code != 200:
        return f"AI 서버 오류: {response.status_code} / {response.text}"

    data = response.json()
    return data["choices"][0]["message"]["content"]


# ======================
# AI 채팅
# ======================
def chat(messages):
    system_message = {
        "role": "system",
        "content": """
너는 AI 학습 플래너이다.

사용자의 공부 관련 질문에 답변하고
공부 방법, 일정 관리, 학습 전략을 추천한다.
"""
    }

    payload = {
        "model": MODEL,
        "messages": [system_message] + messages
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(
        MLAPI_URL,
        json=payload,
        headers=headers
    )

    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    if response.status_code != 200:
        return f"AI 서버 오류: {response.status_code} / {response.text}"

    data = response.json()
    return data["choices"][0]["message"]["content"]