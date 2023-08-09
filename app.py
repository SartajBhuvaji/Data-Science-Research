from flask import Flask, redirect, url_for, render_template, request
import pandas as pd
import scripts.main as script
import time

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

        print("GOING FROM APP")
        synthetic_df = script.function(df, minority_class, algorithm)s
        synthetic_csv_path = "synthetic_data.csv"
        synthetic_df.to_csv(synthetic_csv_path, index=False)

        return redirect(url_for("download_page"))

    else:
        return render_template("home.html")

@app.route("/download")
def download_page():
    return render_template("download.html")

@app.route("/download_synthetic_data")
def download_synthetic_data():
    synthetic_csv_path = "synthetic_data.csv"
    return send_file(synthetic_csv_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
