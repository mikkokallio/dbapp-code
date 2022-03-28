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
    if not session["username"]:
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
        return redirect("/users")
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


@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", name=request.form["name"])


@app.route("/order")
def order():
    return render_template("order.html")


@app.route("/ordered", methods=["POST"])
def ordered():
    pizza = request.form["pizza"]
    extras = request.form.getlist("extra")
    message = request.form["message"]
    return render_template("ordered.html", pizza=pizza,
                           extras=extras,
                           message=message)
