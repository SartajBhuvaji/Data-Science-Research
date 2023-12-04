from autoencoder import generate_autoencoder
import pandas as pd
from tensorflow import keras

def generate_synthetic_data(model_name: str, original_df, minority_class_column: str = 'class', 
                            minority_class_label: str = '0', decoder_activation: str = 'sigmoid', epochs: int = 100, **kwargs):

    print("In generate_synthetic_data")
    if original_df.empty:
        raise ValueError("Empty dataframe.")
    
    if epochs < 1:
        raise ValueError("Invalid number of epochs.")
    
    original_df[minority_class_column] = original_df[minority_class_column].astype(str)  
    minority_df = original_df[original_df[minority_class_column] == minority_class_label]

    if minority_df.empty:
        raise ValueError("Minority class label not found in the dataset.")
    
    majority_df = original_df[original_df[minority_class_column] != minority_class_label]
    minority_df = minority_df.drop(columns=[minority_class_column])
    input_shape = minority_df.shape[1]

    if model_name == 'autoencoder_singleencoder':
        encoder_dense_layers = [20]
        bottle_neck = 16
        decoder_dense_layers = [18, 20]

    elif  model_name == 'autoencoder_balanced': 
        encoder_dense_layers = [22, 20]
        bottle_neck = 16
        decoder_dense_layers = [20, 22]

    elif model_name == 'autoencoder_heavydecoder':
        encoder_dense_layers = [22,20]
        bottle_neck = 16
        decoder_dense_layers = [18, 20, 22, 24]

    elif model_name == 'custom_autoencoder':  
        encoder_dense_layers = kwargs.get('encoder_dense_layers')
        bottle_neck = kwargs.get('bottle_neck')
        decoder_dense_layers = kwargs.get('decoder_dense_layers')    

    else:
        raise ValueError("Invalid model name.") 
    
    try:

        autoencoder, encoder, decoder = generate_autoencoder(input_shape, encoder_dense_layers=encoder_dense_layers,
                                                            bottle_neck=bottle_neck, 
                                                            decoder_dense_layers=decoder_dense_layers,
                                                            decoder_activation=decoder_activation)
    except ValueError:
        raise ValueError("Invalid model parameters.")
    
    print("FITTING AUTOENCODER", epochs)
    opt = keras.optimizers.Adam(learning_rate=0.001)
    autoencoder.compile(optimizer=opt, loss='mse')

    batch_size = 16
    validation_split = 0.25

    data_types = minority_df.dtypes
    print("DATA TYPES PER COLUMN", data_types)

    autoencoder.fit(minority_df, minority_df, epochs=epochs, 
                    batch_size=batch_size, validation_split=validation_split, verbose=0)
    
    class_count_diff = majority_df.shape[0] - minority_df.shape[0]

    generated_data = pd.DataFrame()  
    while generated_data.shape[0] < class_count_diff:
        generated_samples = autoencoder.predict(minority_df, verbose=0)  # Generate synthetic samples
        generated_data = pd.concat([generated_data, pd.DataFrame(generated_samples, columns=minority_df.columns)], ignore_index=True)

    #generated_data = generated_data[:class_count_diff]
    #reshaped_data = generated_data.to_numpy().reshape(len(minority_df), -1)
    df_generated = pd.DataFrame(generated_data, columns = minority_df.columns)

    if minority_class_label.isnumeric():
        df_generated[minority_class_column] = int(minority_class_label)
    else:
        df_generated[minority_class_column] = minority_class_label
        
    minority_df[minority_class_column] = minority_class_label
    synthetic_df = pd.concat([minority_df, df_generated, majority_df], ignore_index=True)
    synthetic_df = synthetic_df.sample(frac=1).reset_index(drop=True)

    print("RETURNING")
    return synthetic_df