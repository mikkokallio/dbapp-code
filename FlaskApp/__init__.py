import os
from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["myAppSetting"]
db = SQLAlchemy(app)

@app.route("/")
def list_users():
    result = db.session.execute("SELECT name FROM users")
    users = result.fetchall()
    return render_template("users.html", count=len(users), users=users) 

#@app.route("/new")
#def new():
#    return render_template("new.html")

#@app.route("/send", methods=["POST"])
#def send():
#    content = request.form["content"]
#    sql = "INSERT INTO messages (content) VALUES (:content)"
#    db.session.execute(sql, {"content":content})
#    db.session.commit()
#    return redirect("/")



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
