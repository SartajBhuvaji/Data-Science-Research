# yourapp/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .scripts import main as script
from .scripts import validate
from .scripts.visualization import visualize
import os
import pandas as pd

data_processed = False
image_directory = os.path.join(os.getcwd(), 'yourapp/static/graphs')

def home(request):
    global data_processed
    if request.method == "POST":
        minority_class = request.POST.get("minority_class")
        minority_class_column = request.POST.get("minority_class_column")
        algorithm = request.POST.get("algorithm")
        csv_file = request.FILES.get("csv_file")

        if csv_file is None or not csv_file.name.endswith(".csv"):
            return redirect('error', error_message="No CSV file uploaded")

        input_df = pd.read_csv(csv_file)
        validation_code, message = validate.validate_input(input_df, minority_class, minority_class_column)
        if validation_code == 0:
            return redirect('error', error_message=message)

        status_code = script.function(input_df, minority_class, minority_class_column, algorithm)
        if status_code == 1:
            data_processed = True
            return redirect('download')
        else:
            return redirect('error', error_message="Internal Error, Please try again.")

    return render(request, "templates/index.html")

def error(request):
    error_message = request.GET.get("error_message", "Internal Error, Please try again.")
    return render(request, "yourapp/error.html", {"message": error_message})

def custom_autoencoder(request):
    global data_processed
    if request.method == "POST":
        minority_class = request.POST.get("minority_class")
        minority_class_column = request.POST.get("minority_class_column")
        csv_file = request.FILES.get("csv_file")
        encoder_dense_layers = request.POST.get("encoder_dense_layers")
        bottle_neck = request.POST.get("bottle_neck")
        decoder_dense_layers = request.POST.get("decoder_dense_layers")
        epochs = request.POST.get("epochs")
        decoder_activation = request.POST.get("decoder_activation")

        if csv_file is None or not csv_file.name.endswith(".csv"):
            return redirect('error', error_message="No CSV file uploaded")

        input_df = pd.read_csv(csv_file)
        validation_code, message = validate.validate_input(
            input_df, minority_class, minority_class_column,
            custom=True, algorithm="autoencoder",
            encoder_dense_layers=encoder_dense_layers,
            bottle_neck=bottle_neck,
            decoder_dense_layers=decoder_dense_layers,
            epochs=epochs
        )

        if validation_code == 0:
            return redirect('error', error_message=message)

        try:
            status_code = script.function(
                input_df, minority_class, minority_class_column,
                algorithm="custom_autoencoder",
                encoder_dense_layers=encoder_dense_layers,
                bottle_neck=bottle_neck,
                decoder_dense_layers=decoder_dense_layers,
                epochs=epochs, decoder_activation=decoder_activation
            )
        except Exception as e:
            print(e)
            return redirect('error', error_message="Internal Error, Please try again.")

        if status_code == 1:
            data_processed = True
            return redirect('download')

    return render(request, "yourapp/custom_autoencoder.html")

def download(request):
    global data_processed
    if data_processed:
        return render(request, "yourapp/download.html")
    else:
        return redirect('home')

def visualization(request):
    if request.method == "POST":
        minority_class = request.POST.get("minority_class")
        minority_class_column = request.POST.get("minority_class_column")
        original_file = request.FILES.get("original_file")
        synthetic_file = request.FILES.get("synthetic_file")
        pure_files_checkbox = request.POST.get("pure_files")
        pure_files_checkbox = True if pure_files_checkbox else False

        if original_file is None or not original_file.name.endswith(".csv") or synthetic_file is None or not synthetic_file.name.endswith(".csv"):
            return redirect('error', error_message="No CSV file uploaded")

        original_df = pd.read_csv(original_file)
        synthetic_df = pd.read_csv(synthetic_file)

        validation_code_1, message_1 = validate.validate_input(original_df, minority_class, minority_class_column)
        validation_code_2, message_2 = validate.validate_input(synthetic_df, minority_class, minority_class_column)

        if validation_code_1 == 0:
            return redirect('error', error_message=message_1)
        if validation_code_2 == 0:
            return redirect('error', error_message=message_2)

        try:
            status_code = visualize(original_df, synthetic_df, minority_class, minority_class_column, pure_files_checkbox)
        except Exception as e:
            print(e)
            return redirect('error', error_message="Internal Error, Please try again.")

        if status_code == 1:
            image_filenames = ['density_plot.png', 'heatmap_plot.png', 'scatter_plot.png']
            return render(request, 'yourapp/visualization_plot.html', {'image_filenames': image_filenames})

    return render(request, "yourapp/visualization.html")

def download_synthetic_data(request):
    if data_processed:
        synthetic_csv_path = "synthetic_data.csv"
        return HttpResponse(synthetic_csv_path, content_type='text/csv')
    else:
        return redirect('home')

def serve_image(request, filename):
    return redirect(os.path.join(image_directory, filename))
