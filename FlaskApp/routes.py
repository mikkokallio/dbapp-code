import json
import secrets
from os import abort
from os import getenv
import requests
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from .app import app
from . import actions


@app.route("/")
def index():
    """Show user's profile unless user hasn't logged in."""
    if "username" in session:
        return redirect("/profile")

    return render_template("index.html", mode="4")


@app.route("/new_place")
def new_place():
    """Show street address selector view."""
    return render_template("pick_place.html")


@app.route("/search_places", methods=["POST"])
def search_places():
    """Fetch addresses based on user input."""
    if "username" not in session:
        return redirect("/")
    location = request.form["location"]
    key = getenv("MAPS_API_KEY")
    url = f"https://atlas.microsoft.com/search/address/json?&subscription-key={key}&api-version=1.0&language=en-US&query={location}"
    response = requests.get(url)
    places = json.loads(response.text)[
        "results"] if response.status_code == 200 else None
    return render_template("pick_place.html", location=location, places=places)


@app.route("/add_place", methods=["POST"])
def add_place():
    """Open form for filling in information about a place."""
    if "username" not in session:
        return redirect("/")
    address = request.form["address"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]
    return render_template("edit_place.html", fields={
        "address": address, "latitude": latitude, "longitude": longitude})


@app.route("/save_place", methods=["POST"])
def save_place():
    """Save submitted place information."""
    if "username" not in session:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    fields = request.form
    messages = actions.validate_place(fields)
    if len(messages) > 0:
        return render_template("edit_place.html", messages=messages, fields=fields)
    messages = actions.save_place(fields)
    if len(messages) == 0:
        return redirect("/places")

    return render_template("edit_place.html", messages=messages, fields=fields)


@app.route("/places")
def list_places():
    """Show a list of all places."""
    if "username" not in session:
        return redirect("/")
    places = actions.get_places()
    return render_template("places.html", places=places, mode="2")


@app.route("/login", methods=["POST"])
def login():
    """Log user in using password and username from form."""
    username = request.form["username"]
    password = request.form["password"]
    user = None
    try:
        user = actions.get_user_by_name(username)
    except AttributeError:
        return render_template("index.html", mode="4",
                               messages=["A problem occurred while fetching user data."])
    if not user:
        return render_template("index.html", mode="4",
                               messages=["Username does not exist"])

    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        session["role"] = user.role
        session["id"] = user.id
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/events")

    return render_template("index.html", mode="4",
                           messages=["Wrong password"])


@app.route("/logout")
def logout():
    """Log user out by removing session data."""
    del session["username"]
    del session["role"]
    del session["id"]
    del session["csrf_token"]
    return redirect("/")


@app.route("/profile")
def show_profile():
    """Show information about user logged in."""
    if "username" not in session:
        return redirect("/")

    user = actions.get_user_by_name(session["username"])
    my_events = actions.get_organized_events_by_user_id(session["id"])
    other_events = actions.get_registered_events_by_user_id(session["id"])
    my_count = len(my_events)
    other_count = len(other_events)
    return render_template("profile.html", user=user, my_events=my_events, mode="1",
                           other_events=other_events, my_count=my_count, other_count=other_count)


@app.route("/new_user")
def new_user():
    """Show form for entering a new username and password."""
    return render_template("new_user.html", fields=None, mode="4")


@app.route("/edit_user")
def edit_user():
    """Show form for filling in other user information."""
    if "username" not in session:
        return redirect("/")
    user = actions.get_user_by_name(session["username"])
    return render_template("edit_user.html", user=user)


@app.route("/add_user", methods=["POST"])
def add_user():
    """Save submitted username and password."""
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]

    messages = []
    messages.extend(actions.validate_username(username))
    messages.extend(actions.validate_password(password))
    if password != password2:
        messages.append("Passwords don't match")

    if len(messages) > 0:
        return render_template("new_user.html", messages=messages, fields=request.form, mode="4")

    hash_value = generate_password_hash(password)
    messages = actions.add_user(username, hash_value)
    if len(messages) == 0:
        session["username"] = username
        session["role"] = "user"
        session["id"] = actions.get_user_by_name(username).id
        session["csrf_token"] = secrets.token_hex(16)
        return render_template("edit_user.html", new_user=True, user=None, mode="4")

    return render_template("new_user.html", messages=messages, fields=request.form, mode="4")


@app.route("/update_user", methods=["POST"])
def update_user():
    """Save submitted user information."""
    if "username" not in session:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    date_of_birth = request.form["date_of_birth"]
    gender = request.form["gender"]
    description = request.form["description"]
    mode = request.form["mode"]

    messages = actions.validate_user(request.form)
    if len(messages) > 0:
        return render_template("edit_user.html", messages=messages, user=request.form, mode=mode)

    messages = actions.update_user(
        session["username"], date_of_birth, gender, description)
    if len(messages) > 0:
        return render_template("edit_user.html", messages=messages, user=request.form, mode=mode)
    
    return redirect("/profile")


@app.route("/new_event")
def new_event():
    """Open form to create new event from scratch."""
    if "username" not in session:
        return redirect("/")
    places = actions.get_places()
    return render_template("edit_event.html", fields=None, places=places, id="")


@app.route("/edit_event", methods=["POST"])
def edit_event():
    """Open event form for editing."""
    if "username" not in session:
        return redirect("/")
    if not request.form["event_id"]:
        return redirect("/events")
    id = request.form["event_id"]
    event = actions.get_event_by_id(id)
    places = actions.get_places()
    if session["username"] != event.username:
        return redirect("/events")
    return render_template("edit_event.html", fields=event, places=places, id=id)


@app.route("/delete_event", methods=["POST"])
def del_event():
    """Delete event using id from currently viewed event."""
    if "username" not in session:
        return redirect("/")
    if not request.form["event_id"]:
        return redirect("/events")
    id = request.form["event_id"]
    messages = actions.delete_event_by_id(id, session["id"])
    events = actions.get_upcoming_events()
    past_events = actions.get_past_events()
    return render_template("events.html", count=len(events), events=events, past_events=past_events,
                           events_view=True, messages=messages)


@app.route("/add_event", methods=["POST"])
def update_event():
    """Save event form fields."""
    if "username" not in session:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    fields = request.form
    places = actions.get_places()

    messages = actions.validate_event(fields)
    if len(messages) > 0:
        return render_template("edit_event.html", messages=messages, fields=fields,
                               places=places, id=fields["event_id"])

    messages = actions.upsert_event(session["id"], fields)
    if len(messages) > 0:
        return render_template("edit_event.html", messages=messages, fields=fields,
                               places=places, id=fields["event_id"])
    
    return redirect("/events")


@app.route("/events")
def list_events():
    """Show a view with past and future events."""
    if "username" not in session:
        return redirect("/")
    events = actions.get_upcoming_events()
    past_events = actions.get_past_events()
    return render_template("events.html", count=len(events), past_count=len(past_events),
                           events=events, past_events=past_events, events_view=True, mode="3")


@app.route("/event/<int:id>")
def show_event(id):
    """Show more detailed information about one event."""
    if "username" not in session:
        return redirect("/")
    event = actions.get_event_by_id(id)
    pos = f"[{event.location[1:-1]}]"
    comments = actions.get_comments_by_event_id(id)
    signups = actions.get_signups_by_event_id(id)
    going = len(signups)
    past = actions.is_past_event(event)
    if session["username"] == event.username:
        user_going = True
    else:
        user_going = actions.get_signup_by_id(id, session["id"])
    return render_template("event.html", id=id, unit=event, comments=comments, signups=signups,
                           pos=pos, going=going, user_going=user_going, past=past,
                           key=getenv("MAPS_API_KEY"))


@app.route("/write_comment", methods=["POST"])
def send_comment():
    """Save a new comment."""
    if "username" not in session:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    event_id = request.form["event_id"]
    comment = request.form["comment"]
    if len(comment) > 0:
        actions.send_comment(event_id, session["id"], comment)
    return redirect(f"/event/{event_id}")


@app.route("/signup", methods=["POST"])
def sign_up():
    """Save registration to event or remove it."""
    if "username" not in session:
        return redirect("/")
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    event_id = request.form["event_id"]
    max_people = request.form["max_people"]
    signups = len(actions.get_signups_by_event_id(event_id))
    actions.add_or_remove_signup(event_id, session["id"], max_people, signups)
    return redirect(f"/event/{event_id}")
