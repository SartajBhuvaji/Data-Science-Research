from flask import Flask, redirect, url_for, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        minority_class = request.form.get("minority_class")
        algorithm = request.form.get("algorithm")
        csv_file = request.files.get("csv_file")

        df = pd.read_csv(csv_file)
        print("Minority Class:", minority_class)
        print("Algorithm:", algorithm)
        print(df.head())

        return redirect(url_for("user", usr = "success"))
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
