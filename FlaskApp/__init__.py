from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

print(getenv("SQL_URI"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQL_URI")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

# @app.route("/")
# def list_users():
#    result = db.session.execute("SELECT name, created_at FROM users")
#    users = result.fetchall()
#    return render_template("users.html", count=len(users), users=users)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
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
        sql = "INSERT INTO users (username, age, gender, role, password, created_at) VALUES (:username, 0, 'male', 'admin', :password, NOW());"
        #sql = "INSERT INTO messages (content) VALUES (:content)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/new_user")


@app.route("/user/<int:id>")
def user(id):
    sql = "SELECT username, age, gender FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    user = result.fetchone()
    print(user)
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


if __name__ == "__main__":
    app.run()
