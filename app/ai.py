from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_plan(subject, exam_date, study_time, goal):

    prompt = f"""
    과목 : {subject}

    시험일 : {exam_date}

    하루 공부시간 : {study_time}

    목표 : {goal}

    공부 계획을 날짜별로 작성해줘.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"system",
                "content":"너는 공부계획을 잘 세워주는 AI이다."
            },
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content