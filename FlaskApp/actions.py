from .db import db


def validate_password(password):
    return len(password) >= 6


def get_user_by_name(username):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def get_user_by_id(id):
    sql = "SELECT username, date_of_birth, gender FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


def get_all_users():
    result = db.session.execute("SELECT username, date_of_birth, gender, description, role, created_at FROM users")
    return result.fetchall()


def add_user(username, hash_value):
    sql = "INSERT INTO users (username, role, password, created_at) VALUES (:username, 'user', :password, NOW());"
    try:
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except: # TODO: Should include exception type!
        return False
    return True

def update_user(username, date_of_birth, gender, description):
    sql = "UPDATE users SET date_of_birth = :date_of_birth, gender = :gender, description = :description WHERE username = :username;"

    try:
        db.session.execute(sql, {"username": username, "date_of_birth": date_of_birth, "gender": gender, "description": description})
        db.session.commit()
    except Exception as e: # TODO: Should include exception type!
        print(e)
        return False
    return True
