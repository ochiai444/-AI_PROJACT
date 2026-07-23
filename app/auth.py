from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

# 기존에 하드코딩되어 있던 시크릿 키 대신 환경변수를 사용하도록 변경
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-for-local")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)




# 비밀번호 암호화

def hash_password(password):

    return pwd_context.hash(password)




# 비밀번호 검증

def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )





# JWT 생성

def create_token(username):

    payload = {

        "sub": username,

        "exp": datetime.utcnow()
        + timedelta(hours=1)

    }


    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )





# JWT 해석

def decode_token(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload


    except JWTError:

        return None