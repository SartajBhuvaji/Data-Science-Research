import pandas as pd

def validate_input(input_df, minority_class, minority_class_column, custom=False, **kwargs):
    df = input_df.copy()
    print("in validate input")
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

    if custom:
        print("in custom")
        if kwargs.get("algorithm") == "autoencoder":
            kwargs.get("encoder_dense_layers")
            encoder_dense_layers = kwargs.get("encoder_dense_layers")
            bottle_neck = kwargs.get("bottle_neck")
            decoder_dense_layers = kwargs.get("decoder_dense_layers")
            epochs = kwargs.get("epochs")

            if encoder_dense_layers == None or encoder_dense_layers == "":
                return (0, "Encoder Dense Layers cannot be empty")
            for num in encoder_dense_layers.strip().split(','):
                if not num.isdigit():
                    return (0, "Encoder Dense Layers should be comma separated integers")
            if bottle_neck == None or bottle_neck == "":
                return (0, "Bottle Neck cannot be empty")
            if len(bottle_neck.split(',')) > 1:
                return (0, "Bottle Neck cannot have more than one value")
            if not bottle_neck.strip().isdigit():
                return (0, "Bottle Neck should be an integer")
            if decoder_dense_layers == None or decoder_dense_layers == "":
                return (0, "Decoder Dense Layers cannot be empty")
            for num in decoder_dense_layers.strip().split(','):
                if not num.isdigit():
                    return (0, "Decoder Dense Layers should be comma separated integers")
                
            if epochs == None or epochs == "":
                return (0, "Epochs cannot be empty")
            
            if not epochs.strip().isdigit():
                return (0, "Epochs should be an integer")

        # if kwargs.get("algorithm") == "your_algorithm":
        #     pass

        
    return (1, "Validated")
