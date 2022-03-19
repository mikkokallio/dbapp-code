import os
from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["myAppSetting"]
db = SQLAlchemy(app)

@app.route("/")
def list_users():
    result = db.session.execute("SELECT name, created_at FROM users")
    users = result.fetchall()
    return render_template("users.html", count=len(users), users=users) 

@app.route("/new_user")
def new_user():
    return render_template("new_user.html")

@app.route("/add_user", methods=["POST"])
def add_user():
    content = request.form["content"]
    sql = "INSERT INTO users (name, age, gender, role, password, created_at) VALUES ('Jorma', 25, 'male', 'admin', 'password123', NOW());"
    #sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/")



#@app.route("/")
#def index():
#    return render_template("index.html")


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


@app.route("/beer")
def beer():
    words = ["bisse", "kalija", "ölppä"]
    return render_template("beers.html", message="Tervetuloa!", items=words)


@app.route("/test")
def test():
    content = ""
    for i in range(100):
        content += str(i + 1) + " "
    return content


@app.route("/page/<int:id>")
def page(id):
    return "Tämä on sivu " + str(id)


@app.route("/hello/<name>", methods=['GET'])
def hello(name: str):
    return f"hello {name}"


if __name__ == "__main__":
    app.run()
