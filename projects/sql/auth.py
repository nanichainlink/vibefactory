from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from models import User

def register_user(db: Session, username: str, email: str, password: str) -> bool:
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        return False  # Usuario ya existe
    hashed_password = generate_password_hash(password, method='sha256')
    user = User(username=username, email=email, password=hashed_password)
    db.add(user)
    db.commit()
    return True

def authenticate_user(db: Session, username: str, password: str) -> bool:
    user = db.query(User).filter_by(username=username).first()
    if not user:
        return False
    return check_password_hash(user.password, password)