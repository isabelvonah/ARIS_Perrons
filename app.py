from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/kuchen")
def kuchen():
    return render_template("kuchen.html")

app.run(debug=True)