from datetime import date, datetime
from sqlalchemy.exc import IntegrityError, OperationalError
import requests
from .db import db


def validate_password(password):
    """Check that password meets all requirements."""
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
    """Check that username meets all requirements."""
    errors = []
    if len(username) < 3 or len(username) > 20:
        errors.append("Username should be 3-20 characters long")
    if any(character.isspace() for character in username):
        errors.append("Username should not contain spaces")
    return errors


def validate_event(fields):
    """Check that event's all information meets requirements."""
    print(fields)
    errors = []
    if len(fields["title"]) < 5 or len(fields["title"]) > 25:
        errors.append("Title must be at 5-25 characters long")
    if not fields["time"]:
        errors.append("Event must have a starting time")
    if "place" not in fields:
        errors.append("Event must have a place")
    if fields["date"] == "":
        errors.append("Event must have a date")
    elif date.today() > datetime.strptime(fields["date"], "%Y-%m-%d").date():
        errors.append("Event can't happen in the past")
    if len(fields["description"].split(" ")) < 5:
        errors.append("Description must be at least 5 words")
    return errors


def validate_place(fields):
    """Check that place's all information meets requirements."""
    errors = []
    if len(fields["name"]) < 5 or len(fields["name"]) > 20:
        errors.append("Name must be 5-20 characters long")
    try:
        if not fields["pic_url"].startswith("https://"):
            errors.append("Each URL should begin with https://")
        elif requests.get(fields["pic_url"]).status_code != 200:
            errors.append("Invalid picture URL")
    except:
        errors.append("Invalid picture URL")
    try:
        if not fields["page_url"].startswith("https://"):
            errors.append("Each URL should begin with https://")
        elif requests.get(fields["page_url"]).status_code != 200:
            errors.append("Invalid web page URL")
    except:
        errors.append("Invalid web page URL")
    if not any([fields["pic_url"].endswith(filetype) for filetype in ["jpg", "png", "gif"]]):
        errors.append("Picture URL should point to a jpg, png, or gif image file")
    if len(fields["description"].split(" ")) < 5:
        errors.append("Description must be at least 5 words")
    return errors


def validate_user(fields):
    """Check that user's information meets requirements."""
    errors = []
    if fields["date_of_birth"] == "":
        errors.append("User must have a date of birth")
    elif date.today() < datetime.strptime(fields["date_of_birth"], "%Y-%m-%d").date():
        errors.append("Date of birth can't be in the future")
    if len(fields["description"].split(" ")) < 5:
        errors.append("Description must be at least 5 words")
    return errors


def is_past_event(event):
    """Check if event occurred in past."""
    return date.today() > event["date"]


def get_user_by_name(username):
    """Fetch one user with a specific name."""
    sql = """SELECT id, username, date_of_birth, gender, description, created_at, password, role
             FROM users WHERE username=:username;"""
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def get_user_by_id(id):
    """Fetch one user based on id."""
    sql = "SELECT username, date_of_birth, gender FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


def add_user(username, hash_value):
    """Add a new user's information."""
    sql = """INSERT INTO users (username, role, password, created_at)
             VALUES (:username, 'user', :password, NOW());"""
    try:
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except (AttributeError, OperationalError):
        return ["An error with saving the data occurred. Please try again later."]
    except IntegrityError:
        return ['That username already exists.']
    return []


def update_user(username, date_of_birth, gender, description):
    """Change an existing user's information."""
    sql = """UPDATE users SET date_of_birth = :date_of_birth, gender = :gender,
             description = :description WHERE username = :username;"""

    try:
        db.session.execute(sql, {"username": username, "date_of_birth": date_of_birth,
                           "gender": gender, "description": description})
        db.session.commit()
    except (AttributeError, OperationalError):
        return ["An error with saving the data occurred. Please try again later."]
    return []


def save_place(fields):
    """Save info from form about a new place."""
    sql = """INSERT INTO places (name, location, address, description,
             page_url, pic_url, created_at)
             VALUES (:name, POINT(:longitude, :latitude), :address,
             :description, :page_url, :pic_url, NOW());"""
    try:
        db.session.execute(sql, {
            "name": fields["name"],
            "longitude": float(fields["longitude"]),
            "latitude": float(fields["latitude"]),
            "address": fields["address"],
            "description": fields["description"],
            "page_url": fields["page_url"],
            "pic_url": fields["pic_url"]})
        db.session.commit()
    except (AttributeError, OperationalError):
        return ["An error with saving the data occurred. Please try again later."]
    except IntegrityError:
        return ['That name already exists.']
    return []


def get_places():
    """Fetch all places in database."""
    sql = """SELECT id, pic_url, address, description, name, page_url,
             LEFT(page_url, 35) AS short_url FROM places ORDER BY name ASC;"""
    result = db.session.execute(sql)
    return result.fetchall()


def get_events_by_place(id):
    """Fetch events organized at a particular place."""
    sql = "SELECT COUNT(*) AS count FROM events WHERE place_id = :id;"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


def delete_place_by_id(id):
    """Remove one place based on id provided that no event uses that place."""
    event_count = get_events_by_place(id).count
    if event_count > 0:
        return [f"This place has {event_count} event(s). You must delete them first."]
    sql = "DELETE FROM places WHERE id = :id;"
    db.session.execute(sql, {"id": id})
    db.session.commit()
    return ["Place deleted."]


def upsert_event(user_id, fields):
    """Add new or update existing event's information."""
    if fields["event_id"] != "":
        sql = """UPDATE events SET title = :title, place_id = :place_id, date = :date, time = :time,
                 max_people = :max_people, description = :description WHERE id = :id;"""
    else:
        sql = """INSERT INTO events (title, host_id, place_id, date, time,
                 max_people, description, created_at) VALUES (
                 :title, :host_id, :place_id, :date, :time, :max_people, :description, NOW());"""
    try:
        db.session.execute(sql, {
            "title": fields["title"],
            "host_id": user_id,
            "place_id": fields["place"],
            "date": fields["date"],
            "time": fields["time"],
            "max_people": fields["max_people"],
            "description": fields["description"],
            "id": fields["event_id"]})
        db.session.commit()
    except (AttributeError, OperationalError):
        return ["An error with saving the data occurred. Please try again later."]
    return []


def get_comments_by_event_id(id):
    """Fetch all comments about one event."""
    sql = """SELECT users.username as username, comment, comments.created_at AS created_at, gender,
             users.description AS about_me, users.created_at AS member_since FROM comments
             LEFT JOIN users ON comments.user_id = users.id
             WHERE event_id=:id ORDER BY created_at DESC;"""
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


def get_signups_by_event_id(id):
    """Fetch all registrations for one event."""
    sql = """SELECT username, user_id FROM signups LEFT JOIN users ON signups.user_id = users.id
             WHERE event_id=:id;"""
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


def get_registered_events_by_user_id(id):
    """Fetch which events a particular user is going to."""
    sql = """SELECT events.id AS id, title, date, gender, users.description AS about_me,
             places.pic_url AS pic_url, places.name AS place, users.created_at AS member_since,
             users.username AS username FROM signups
             LEFT JOIN events ON signups.event_id = events.id
             LEFT JOIN users ON events.host_id = users.id
             LEFT JOIN places ON events.place_id = places.id
             WHERE signups.user_id = :id ORDER BY events.date DESC;"""
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


def get_organized_events_by_user_id(id):
    """Fetch all events a particular user has created."""
    sql = """SELECT events.id AS id, title, date, gender, users.description AS about_me,
             places.pic_url AS pic_url, places.name AS place, users.created_at AS member_since,
             users.username as username FROM events
             LEFT JOIN users ON events.host_id = users.id
             LEFT JOIN places ON events.place_id = places.id
             WHERE events.host_id = :id ORDER BY events.date DESC;"""
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


def get_upcoming_events():
    """Fetch all events happening in the future."""
    sql = """SELECT events.id AS id, title, date, gender, users.description AS about_me,
             places.pic_url AS pic_url, places.name AS place, users.created_at AS member_since,
             users.username AS username FROM events
             LEFT JOIN users ON events.host_id = users.id
             LEFT JOIN places ON events.place_id = places.id
             WHERE events.date >= NOW() ORDER BY events.date ASC;"""
    result = db.session.execute(sql)
    return result.fetchall()


def get_past_events():
    """Fetch all events that have already happened."""
    sql = """SELECT events.id AS id, title, date, gender, users.description AS about_me,
             places.pic_url AS pic_url, places.name AS place, users.created_at AS member_since,
             users.username AS username FROM events
             LEFT JOIN users ON events.host_id = users.id
             LEFT JOIN places ON events.place_id = places.id
             WHERE events.date < NOW() ORDER BY events.date DESC;"""
    result = db.session.execute(sql)
    return result.fetchall()


def get_event_by_id(id):
    """Fetch one event based on id."""
    sql = """SELECT events.id AS id, events.description AS description, title, date, time, pic_url,
             max_people, address, page_url, LEFT(page_url, 35) AS short_url, place_id, name,
             gender, location, users.description AS about_me, users.created_at AS member_since,
             users.username as username FROM events
             LEFT JOIN users ON events.host_id = users.id
             LEFT JOIN places ON events.place_id = places.id
             WHERE events.id=:id;"""
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()


def delete_event_by_id(id, user_id):
    """Remove one event based on id."""
    sql = "DELETE FROM events WHERE id = :id AND host_id = :user_id RETURNING title;"
    db.session.execute(sql, {"id": id, "user_id": user_id})
    db.session.commit()
    return ["Event deleted."]


def send_comment(event_id, user_id, comment):
    """Add a comment to a particular event."""
    sql = """INSERT INTO comments (event_id, user_id, comment, created_at)
             values (:event_id, :user_id, :comment, NOW());"""
    try:
        db.session.execute(
            sql, {"event_id": event_id, "user_id": user_id, "comment": comment})
        db.session.commit()
    except (AttributeError, OperationalError):
        return ["An error with saving the data occurred. Please try again later."]
    return []


def get_signup_by_id(event_id, user_id):
    """Check if a particular user is going to an event."""
    sql = "SELECT COUNT(*) FROM signups WHERE event_id=:event_id AND user_id=:user_id;"
    result = db.session.execute(
        sql, {"event_id": event_id, "user_id": user_id})
    return result.fetchone().count > 0


def add_or_remove_signup(event_id, user_id, max_people, signups):
    """Add a registration to event, or remove it if already exists."""
    if get_signup_by_id(event_id, user_id):
        sql = "DELETE FROM signups WHERE event_id=:event_id AND user_id=:user_id;"
    else:
        if max_people != "None" and signups >= int(max_people) - 1:
            return
        sql = """INSERT INTO signups (event_id, user_id, created_at)
                 values (:event_id, :user_id, NOW());"""
    try:
        db.session.execute(sql, {"event_id": event_id, "user_id": user_id})
        db.session.commit()
    except Exception:
        return
    return
