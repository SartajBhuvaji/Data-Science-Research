import os
import scripts.autoencoder_model as autoencoder_model
import scripts.ikc as IKC_model
# import your function from scripts. here #Do not remove this line, add your code above

def function(input_df, minority_class, minority_class_column, algorithm, **kwargs):
    # Housekeeping
    print("Housekeeping")
    path = os.path.join(os.getcwd(), 'static', 'output')
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")
    #Dont change code above this line, create a synthetic_df which would be returned


    autoencoders = ['autoencoder_singleencoder', 'autoencoder_balanced', 'autoencoder_heavydecoder']
    if algorithm in autoencoders:
        try:
            model_name = algorithm
            print("Calling generate_synthetic_data")
            synthetic_df = autoencoder_model.generate_synthetic_data(model_name=model_name,original_df = input_df, 
                                    minority_class_column = minority_class_column,
                                    minority_class_label = minority_class, 
                                    decoder_activation = 'sigmoid', epochs = 200)
        except Exception as e:
            print(f"Error in autoencoder: {e}")
            return 0    
        
    elif algorithm == "custom_autoencoder":
        try:
            model_name = "custom_autoencoder"
            encoder_dense_layers_str = kwargs.get('encoder_dense_layers')
            encoder_dense_layers = [int(val) for val in encoder_dense_layers_str.split(",")]

            bottle_neck_str = kwargs.get('bottle_neck')
            bottle_neck = int(bottle_neck_str)

            decoder_dense_layers_str = kwargs.get('decoder_dense_layers')
            decoder_dense_layers = [int(val) for val in decoder_dense_layers_str.split(",")]

            decoder_activation = kwargs.get('decoder_activation') 
            epochs_str = kwargs.get('epochs')
            epochs = int(epochs_str)

            synthetic_df = autoencoder_model.generate_synthetic_data(model_name=model_name,original_df = input_df, 
                                    minority_class_column = minority_class_column, minority_class_label = minority_class,
                                    decoder_activation = decoder_activation, epochs = epochs,

                                    encoder_dense_layers=encoder_dense_layers,
                                    bottle_neck = bottle_neck, decoder_dense_layers = decoder_dense_layers)
            
        except Exception as e:
            print(f"Error in autoencoder: {e}")
            return 0    
    
    if algorithm == "ikc":
        try:
            synthetic_df = IKC_model.IKC(input_df, minority_class_column=minority_class_column, 
                                         minority_class_label=minority_class)
            
        except Exception as e:
            print(f"Error in your algorithm: {e}")
            return 0
    
    '''
    elif:
        try: 
            synthetic_df = your_file.your_algorithm(input_df, minority_class_column=minority_class_column, 
                                                    minority_class_label=minority_class)
        #add your algorithm here (Do not remove this line add your elif statement above this line)

        except Exception as e:
            print(f"Error in your algorithm: {e}")
            return 0
    '''
    
    #Dont change code below this line, create a synthetic_df which would be returned

    synthetic_df.to_csv(os.path.join(path, 'synthetic_data.csv'), index=False)
    return 1 

                      