from app import app
import actions
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/")
# def list_users():
#    result = db.session.execute("SELECT name, created_at FROM users")
#    users = result.fetchall()
#    return render_template("users.html", count=len(users), users=users)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = actions.get_user_by_name(username)
    if not user:
        pass
        # TODO: invalid username
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
        else:
            pass  # TODO: invalid password
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
    if password == password2:
        hash_value = generate_password_hash(password)
        actions.add_user(username, hash_value)
        return redirect("/")
    else:
        return redirect("/new_user")


@app.route("/user/<int:id>")
def user(id):
    user = actions.get_user_by_id(id)
    return render_template("user.html", id=id, user=user)


@app.route("/form")
def form():
    return render_template("form.html")


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


@app.route("/hello/<name>", methods=['GET'])
def hello(name: str):
    return f"hello {name}"
