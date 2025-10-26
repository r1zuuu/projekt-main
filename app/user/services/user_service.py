from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

def create_user(username, password):
    """Tworzy nowego użytkownika"""
    if not username or not password:
        return None, "Brak danych"
    if len(password) < 6:
        return None, "Hasło musi mieć co najmniej 6 znaków"
    if User.query.filter_by(username=username).first():
        return None, "Użytkownik już istnieje"

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return new_user, None


def authenticate_user(username, password):
    """Sprawdza dane logowania"""
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return None, "Nieprawidłowe dane logowania"
    return user, None


def get_user_by_id(user_id):
    """Zwraca użytkownika po ID"""
    return User.query.get(user_id)
