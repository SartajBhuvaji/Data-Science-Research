import pandas as pd
import scripts.autoencoder_model as autoencoder_model

def function(file, minority_class, algorithm):
    if algorithm == "autoencoder":
        print("Autoencoder")
        #def generate_synthetic_data(model_name: str, original_df, minority_class_column: str = 'class', minority_class_label: str = '0', decoder_activation: str = 'sigmoid', epochs: int = 100)
        model_name = 'single_encoder'
        print("Calling generate_synthetic_data")
        synthetic_df = autoencoder_model.generate_synthetic_data(model_name=model_name,original_df = file, minority_class_column = 'class',
                                minority_class_label = minority_class, decoder_activation = 'sigmoid', epochs = 200)

        return synthetic_df
        #synthetic_df.to_csv("synthetic_data.csv", index=False)
        # give user the option to download the file                        
