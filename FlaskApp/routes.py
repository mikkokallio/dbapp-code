from .app import app
from . import actions
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def index():
    if "username" in session:
        return redirect("/profile")

    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = actions.get_user_by_name(username)
    if not user:
        return render_template("index.html", messages=["Username does not exist"])
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["role"] = user.role
            session["id"] = user.id
        else:
            return render_template("index.html", messages=["Wrong password"])
    return redirect("/events")


@app.route("/logout")
def logout():
    del session["username"]
    del session["role"]
    return redirect("/")


@app.route("/profile")
def show_profile():
    if "username" not in session:
        return redirect("/")

    user = actions.get_user_by_name(session["username"])
    return render_template("profile.html", user=user)


@app.route("/new_user")
def new_user():
    return render_template("new_user.html")


@app.route("/edit_user")
def edit_user():
    user = actions.get_user_by_name(session["username"])
    return render_template("edit_user.html", user=user)


@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]

    messages = []
    messages.extend(actions.validate_username(username))
    messages.extend(actions.validate_password(password))
    if password != password2:
        messages.append("Passwords don't match")

    if len(messages) > 0:
        return render_template("new_user.html", messages=messages, fields=request.form)

    hash_value = generate_password_hash(password)
    if actions.add_user(username, hash_value):
        session["username"] = username
        session["role"] = "user"
        return render_template("edit_user.html", new_user=True, user=None)
    else:
        return render_template("new_user.html", messages=[f"Can't create user"], fields=request.form)


@app.route("/update_user", methods=["POST"])
def update_user():
    if "username" not in session:
        return redirect("/")

    date_of_birth = request.form["date_of_birth"]
    gender = request.form["gender"]
    description = request.form["description"]

    messages = actions.validate_user(request.form)

    if len(messages) > 0:
        return render_template("edit_user.html", messages=messages, user=request.form)
    if actions.update_user(session["username"], date_of_birth, gender, description):
        return redirect("/profile")
    else:
        return render_template("edit_user.html", messages=[f"Failed to save changes, please check the values"], user=request.form)


@app.route("/new_event")
def new_event():
    if "username" not in session:
        return redirect("/")
    return render_template("new_event.html", fields=None)


@app.route("/add_event", methods=["POST"])
def update_event():
    if "username" not in session:
        return redirect("/")

    fields = request.form
    messages = actions.validate_event(fields)
    if len(messages) > 0:
        return render_template("new_event.html", messages=messages, fields=fields)
    if actions.upsert_event(session["username"], fields):
        return redirect("/events")
    else:
        return render_template("new_event.html", messages=[f"Failed to save changes, please check the values"], fields=fields)


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
