from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", name=request.form["name"])

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