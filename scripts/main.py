import pandas as pd
import os
import scripts.autoencoder_model as autoencoder_model
# import your function from scripts. here #Do not remove this line, add your code above

def function(file, minority_class, minority_class_column, algorithm):

    autoencoders = ['autoencoder_singleencoder', 'autoencoder_balanced', 'autoencoder_heavydecoder']
    if algorithm in autoencoders:
        print("Autoencoder")
        model_name = algorithm

        print("Calling generate_synthetic_data")
        synthetic_df = autoencoder_model.generate_synthetic_data(model_name=model_name,original_df = file, 
                                minority_class_column = minority_class_column,
                                minority_class_label = minority_class, 
                                decoder_activation = 'sigmoid', epochs = 200)

    #elif:
        #add your algorithm here (Do not remove this line add your elif statement above this line)

    #Dont change code below this line, create a synthetic_df which would be returned
    path = os.path.join(os.getcwd(), 'static', 'output')
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")

    synthetic_df.to_csv(os.path.join(path, 'synthetic_data.csv'), index=False)
    return 1                       

def testfunctionn():
    print("IN MAIN.py")