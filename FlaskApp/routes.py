from xml.etree.ElementTree import Comment
from .app import app
from . import actions
from datetime import date
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = actions.get_user_by_name(username)
    print(user)
    if not user:
        return render_template("index.html", message="Username does not exist")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["role"] = user.role
        else:
            return render_template("index.html", message="Wrong password")
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/new_user")
def new_user():
    return render_template("new_user.html")


@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]

    if password != password2:
        return render_template("new_user.html", message=f"Passwords don't match")
    if not actions.validate_password(password):
        return render_template("new_user.html", message=f"Password must be at least 6 characters long")

    hash_value = generate_password_hash(password)
    if actions.add_user(username, hash_value):
        session["username"] = username
        session["role"] = "user"
        return render_template("edit_user.html", message=f"New user {username} created")
    else:
        return render_template("new_user.html", message=f"Can't create user")


@app.route("/update_user", methods=["POST"])
def update_user():
    if "username" not in session:
        return redirect("/")

    day = request.form["day"]
    month = request.form["month"]
    year = request.form["year"]
    gender = request.form["gender"]
    description = request.form["description"]

    # TODO: Separate validaton function in actions?
    if not day.isnumeric() or int(day) < 1 or int(day) > 32:
        return render_template("edit_user.html", message=f"Invalid day of birth")
    if not month.isnumeric() or int(month) < 1 or int(month) > 12:
        return render_template("edit_user.html", message=f"Invalid month of birth")
    if not year.isnumeric() or int(year) < 1900 or int(year) > date.today().year - 1:
        return render_template("edit_user.html", message=f"Invalid year of birth")

    if actions.update_user(session["username"], f"{year}-{month}-{day}", gender, description):
        return redirect("/")
    else:
        return render_template("edit_user.html", message=f"Failed to save changes, please check the values")


@app.route("/user/<int:id>")
def user(id):
    user = actions.get_user_by_id(id)
    return render_template("user.html", id=id, user=user)


@app.route("/users")
def list_users():
    users = actions.get_all_users()
    return render_template("users.html", count=len(users), users=users)


@app.route("/new_event")
def new_event():
    if "username" not in session:
        return redirect("/")
    return render_template("new_event.html")


@app.route("/add_event", methods=["POST"])
def update_event():
    if "username" not in session:
        return redirect("/")

    fields = request.form

    # TODO: Create validation functions in actions and add here

    if actions.upsert_event(session["username"], fields):
        return redirect("/events")
    else:
        return render_template("new_event.html", message=f"Failed to save changes, please check the values")


@app.route("/events")
def list_events():
    if "username" not in session:
        return redirect("/")
    events = actions.get_all_events()
    return render_template("events.html", count=len(events), events=events, events_view=True)


@app.route("/event/<int:id>")
def show_event(id):
    if "username" not in session:
        return redirect("/")
    event = actions.get_event_by_id(id)
    comments = actions.get_comments_by_event_id(id)
    signups = actions.get_signups_by_event_id(id)
    going = len(signups)
    if session["username"] == event.username:
        user_going = True
    else:
        user_going = actions.get_signup_by_id(id, session["username"])
    return render_template("event.html", id=id, unit=event, comments=comments, signups=signups, going=going, user_going=user_going)


@app.route("/write_comment", methods=["POST"])
def send_comment():
    if "username" not in session:
        return redirect("/")

    event_id = request.form["event_id"]
    comment = request.form["comment"]
    if len(comment) >= 1:
        actions.send_comment(event_id, session["username"], comment)
    return redirect(f"/event/{event_id}")


@app.route("/signup", methods=["POST"])
def sign_up():
    if "username" not in session:
        return redirect("/")

    event_id = request.form["event_id"]
    actions.add_or_remove_signup(event_id, session["username"])
    return redirect(f"/event/{event_id}")
