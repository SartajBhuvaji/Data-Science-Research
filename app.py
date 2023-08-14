from flask import Flask, redirect, send_file, url_for, render_template, request
import pandas as pd
import scripts.main as script
import time

app = Flask(__name__)
data_processed = False

@app.route("/", methods=["POST", "GET"])
def home():
    global data_processed
    if request.method == "POST":
        minority_class = request.form.get("minority_class")
        minority_class_column = request.form.get("minority_class_column")
        algorithm = request.form.get("algorithm")
        csv_file = request.files.get("csv_file")

        validation_code, message = validate_input(csv_file, minority_class, minority_class_column)
        if validation_code == 0:
            return redirect(url_for("error", error_message=message))

        input_df = pd.read_csv(csv_file)
        print("GOING FROM APP")
        status_code = script.function(input_df, minority_class, minority_class_column, algorithm)
        if status_code == 1:
            data_processed = True
            return redirect(url_for("download"))
    return render_template("index.html")
   

@app.route("/error")
def error():
    error_message = request.args.get("error_message", default="Internal Error, Please try again.")
    return render_template("error.html", message=error_message)


def validate_input(csv_file, minority_class, minority_class_column):
    if not csv_file:
        return (0, "No CSV file uploaded")
    
    if not csv_file.filename.endswith(".csv"):
        return (0, "Invalid CSV file uploaded")

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        return (0, "Invalid CSV file uploaded")

    if df.empty:
        return (0, "Empty DataFrame")
    if minority_class_column not in df.columns:
        return (0, f"Minority Class Column {minority_class_column} not present in the DataFrame") 
       
    unique_values = df[minority_class_column].unique()
    unique_values_as_str = [str(value) for value in unique_values]
    if str(minority_class) not in unique_values_as_str:
        return (0, f"Minority Class '{minority_class}' not present in the DataFrame")  
    
    if df.isnull().values.any():
        return (0, "Missing Values present in the DataFrame")
    return (1, "Validated")


@app.route("/download")
def download():
    global data_processed
    if data_processed:
        return render_template("download.html")
    else:
        return redirect(url_for("home"))

@app.route("/download_synthetic_data")
def download_synthetic_data():
    if data_processed:
        synthetic_csv_path = "synthetic_data.csv"
        return send_file(synthetic_csv_path, as_attachment=True)
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
