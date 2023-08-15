#for testing purposes
from tensorflow import keras

def generate_autoencoder(input_shape, **kwargs):
    '''
    Constructs an autoencoder model using the given input shape and optional parameters.

    Args:
        input_shape (int): The shape of the input data.
        **kwargs: Optional keyword arguments.
            encoder_dense_layers (list): List of units for each dense layer in the encoder. Default is an empty list.
            bottle_neck (int): The dimension of the bottleneck layer. Default is half of the input_shape.
            decoder_dense_layers (list): List of units for each dense layer in the decoder. Default is an empty list.
            decoder_activation (str): Activation function for the decoder output layer. Default is 'sigmoid'.

    Returns:
        tuple: A tuple containing the autoencoder, encoder, and decoder models.
    '''
    print("Generating model structure")
    # Default parameter values
    input_shape = int(input_shape)
    if input_shape < 0:
        raise ValueError("Input shape must be greater than 0.")
    
    encoder_dense_layers = kwargs.get('encoder_dense_layers', [])
    bottle_neck = kwargs.get('bottle_neck', input_shape // 2)
    decoder_dense_layers = kwargs.get('decoder_dense_layers', [])
    decoder_activation = kwargs.get('decoder_activation', 'sigmoid')    
    print("MODEL: " ,encoder_dense_layers, bottle_neck, decoder_dense_layers, decoder_activation)
    
    # Encoder Model
    encoder_input = keras.Input(shape=(input_shape,), name="encoder")
    x = keras.layers.Flatten()(encoder_input)

    # Encoder Dense Layers
    for units in encoder_dense_layers:
        x = keras.layers.Dense(units, activation="relu")(x)

    encoder_output = keras.layers.Dense(bottle_neck, activation="relu")(x)
    encoder = keras.Model(encoder_input, encoder_output, name="encoder")

    # Decoder Model
    decoder_input = keras.Input(shape=(bottle_neck,), name="decoder")
    x = decoder_input

    # Decoder Dense Layers
    for units in decoder_dense_layers:
        x = keras.layers.Dense(units, activation="relu")(x)

    decoder_output = keras.layers.Dense(input_shape, activation=decoder_activation)(x)
    decoder = keras.Model(decoder_input, decoder_output, name="decoder")

    # Autoencoder Model
    autoencoder_input = keras.Input(shape=(input_shape,), name="input")
    encoded = encoder(autoencoder_input)
    decoded = decoder(encoded)
    autoencoder = keras.Model(autoencoder_input, decoded, name="autoencoder")

    return autoencoder, encoder, decoder