from flask import Flask, redirect, send_file, url_for, render_template, request
import pandas as pd
import scripts.main as script
import scripts.validate as validate

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

        if csv_file == None or not str(csv_file.filename).endswith(".csv"):
            return redirect(url_for("error", error_message="No CSV file uploaded"))

        input_df = pd.read_csv(csv_file)
        validation_code, message = validate.validate_input(input_df, minority_class, minority_class_column)
        if validation_code == 0:
           return redirect(url_for("error", error_message=message))
        
        status_code = script.function(input_df, minority_class, minority_class_column, algorithm)
        if status_code == 1:
            data_processed = True
            return redirect(url_for("download"))
        else:
            return redirect(url_for("error", error_message="Internal Error, Please try again."))
    return render_template("index.html")
   

@app.route("/error")
def error():
    error_message = request.args.get("error_message", default="Internal Error, Please try again.")
    return render_template("error.html", message=error_message)


@app.route('/custom_autoencoder', methods=["POST", "GET"])
def custom_autoencoder():
    global data_processed
    if request.method == "POST":
        minority_class = request.form.get("minority_class")
        minority_class_column = request.form.get("minority_class_column")
        csv_file = request.files.get("csv_file")
        encoder_dense_layers = request.form.get("encoder_dense_layers")
        bottle_neck = request.form.get("bottle_neck")
        decoder_dense_layers = request.form.get("decoder_dense_layers")
        epochs = request.form.get("epochs")
        decoder_activation = request.form.get("decoder_activation")

        if csv_file == None or not str(csv_file.filename).endswith(".csv"):
          return redirect(url_for("error", error_message="No CSV file uploaded"))
        
        input_df = pd.read_csv(csv_file)
        validation_code, message = validate.validate_input(input_df, minority_class, minority_class_column, custom=True, algorithm="autoencoder",
                                                  encoder_dense_layers=encoder_dense_layers, bottle_neck=bottle_neck, 
                                                  decoder_dense_layers=decoder_dense_layers, epochs=epochs)                  
        if validation_code == 0:
           return redirect(url_for("error", error_message=message))
        else:
            print("VALDATAED")
        try:
            status_code = script.function(input_df, minority_class, minority_class_column, algorithm="custom_autoencoder", 
                                        encoder_dense_layers=encoder_dense_layers, bottle_neck=bottle_neck,
                                        decoder_dense_layers=decoder_dense_layers, epochs=epochs, decoder_activation=decoder_activation)
        except Exception as e:
            print(e)
            return redirect(url_for("error", error_message="Internal Error, Please try again."))    

        if status_code == 1:
            data_processed = True
            return redirect(url_for("download"))
    return render_template("custom_autoencoder.html")

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
