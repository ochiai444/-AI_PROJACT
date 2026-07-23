from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "local-test-secret-key"
)
ALGORITHM = "HS256"



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