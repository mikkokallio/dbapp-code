from datetime import date, datetime
from .db import db


def validate_password(password):
    errors = []
    if len(password) < 6:
        errors.append("Password should be at least 6 characters")
    if any(character.isspace() for character in password):
        errors.append("Password should not contain spaces")
    if not any(character.isdigit() for character in password):
        errors.append("Password should have at least one number")
    if not any(character.islower() for character in password):
        errors.append("Password should have at least one lowercase letter")
    if not any(character.isupper() for character in password):
        errors.append("Password should have at least one uppercase letter")
    return errors


def validate_username(username):
    errors = []
    if len(username) < 3:
        errors.append("Username should be at least 3 characters")
    if any(character.isspace() for character in username):
        errors.append("Username should not contain spaces")
    return errors


def validate_event(fields):
    errors = []
    if len(fields["title"]) < 5:
        errors.append("Title must be at least 5 characters")
    if fields["date"] == "":
        errors.append("Event must have a date")
    elif date.today() > datetime.strptime(fields["date"], "%Y-%m-%d").date():
        errors.append("Event can't happen in the past")
    if len(fields["description"].split(" ")) < 5:
        errors.append("Description must be at least 5 words")
    return errors


def validate_user(fields):
    errors = []
    if fields["date_of_birth"] == "":
        errors.append("User must have a date of birth")
    elif date.today() < datetime.strptime(fields["date_of_birth"], "%Y-%m-%d").date():
        errors.append("Date of birth can't be in the future")
    if len(fields["description"].split(" ")) < 5:
        errors.append("Description must be at least 5 words")
    return errors


def get_user_by_name(username):
    sql = "SELECT id, username, date_of_birth, gender, description, created_at, password, role FROM users WHERE username=:username"
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


def upsert_event(username, fields):
    sql = "INSERT INTO events (title, host_id, date, time, description, created_at) VALUES (:title, :host_id, :date, :time, :description, NOW());"
    id = get_user_by_name(username).id
    try:
        db.session.execute(sql, {
            "title": fields["title"],
            "host_id": id,
            "date": fields["date"],
            "time": f"{fields['hours']}:{fields['minutes']}",
            "description": fields["description"]})
        db.session.commit()
    except Exception as e: # TODO: Should include exception type!
        print(e)
        return False
    return True


def get_comments_by_event_id(id):
    sql = """SELECT users.username as username, comment, comments.created_at as created_at, gender,
        users.description as about_me, users.created_at as member_since FROM comments
        LEFT JOIN users ON comments.user_id = users.id WHERE event_id=:id ORDER BY created_at DESC"""
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


def get_signups_by_event_id(id):
    sql = "SELECT username, user_id FROM signups LEFT JOIN users ON signups.user_id = users.id WHERE event_id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


def get_all_events():
    sql = """SELECT events.id AS id, title, date, gender, users.description as about_me,
        users.created_at as member_since, users.username as username FROM events
        LEFT JOIN users ON events.host_id = users.id ORDER BY events.date ASC"""
    result = db.session.execute(sql)
    return result.fetchall()


def get_event_by_id(id):
    sql = "SELECT events.id AS id, title, date, time, events.description as description, gender, users.description as about_me, users.created_at as member_since, users.username as username FROM events LEFT JOIN users ON events.host_id = users.id WHERE events.id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


def send_comment(event_id, user, comment):
    sql = "INSERT INTO comments (event_id, user_id, comment, created_at) values (:event_id, :user_id, :comment, NOW());"
    user_id = get_user_by_name(user).id
    print(user_id)
    try:
        db.session.execute(sql, {"event_id": event_id, "user_id": user_id, "comment": comment})
        db.session.commit()
    except Exception as e: # TODO: Should include exception type!
        print(e)
    return


def get_signup_by_id(event_id, username):
    user_id = get_user_by_name(username).id
    sql = "SELECT COUNT(*) FROM signups WHERE event_id=:event_id AND user_id=:user_id"
    result = db.session.execute(sql, {"event_id": event_id, "user_id": user_id})
    return result.fetchone().count > 0 


def add_or_remove_signup(event_id, username):
    user_id = get_user_by_name(username).id
    if get_signup_by_id(event_id, username):
        sql = "DELETE FROM signups WHERE event_id=:event_id AND user_id=:user_id"
    else:
        sql = "INSERT INTO signups (event_id, user_id, created_at) values (:event_id, :user_id, NOW());"
    try:
        db.session.execute(sql, {"event_id": event_id, "user_id": user_id})
        db.session.commit()        
    except Exception as e: # TODO: Should include exception type!
        print(e)
    return
