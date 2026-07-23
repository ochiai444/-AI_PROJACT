from sqlalchemy.orm import Session
from app.models import User
from app.auth import hash_password

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, password: str):
    user = User(
        username=username,
        password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user