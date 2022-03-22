from db import db


def get_user_by_name(username):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def get_user_by_id(id):
    sql = "SELECT username, age, gender FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


def add_user(username, hash_value):
    sql = "INSERT INTO users (username, age, gender, role, password, created_at) VALUES (:username, 0, 'male', 'admin', :password, NOW());"
    #sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()
