import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("MLAPI_BASE_URL")
)



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


    response = client.chat.completions.create(

        model="openai/gpt-5-mini",

        messages=[

            {
                "role":"system",
                "content":
                "너는 학습 계획을 전문적으로 작성해주는 AI 스터디 플래너이다."
            },

            {
                "role":"user",
                "content":prompt
            }

        ]

    )


    return response.choices[0].message.content





# ======================
# AI 채팅
# ======================

def chat(messages):


    system_message = {

        "role":"system",

        "content":
        """
너는 AI 학습 플래너이다.

사용자의 공부 관련 질문에 답변하고,
필요하면 공부 방법, 일정 관리, 학습 전략을 추천한다.
"""
    }



    response = client.chat.completions.create(

        model="openai/gpt-5-mini",


        messages=[
            system_message
        ] + messages

    )


    return response.choices[0].message.content