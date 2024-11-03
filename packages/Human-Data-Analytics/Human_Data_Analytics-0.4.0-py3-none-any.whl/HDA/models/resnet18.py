from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dense, Add, ReLU, Concatenate
from tensorflow.keras.layers import BatchNormalization
from .cbam import cbam_block


# Basic Identity Block (used in ResNet)
def identity_block(X, f, filters):
    F1, F2 = filters

    # Save the input value for adding back after passing through the layers
    X_shortcut = X

    # First component of main path
    X = Conv2D(filters=F1, kernel_size=(3, 3), strides=(1, 1), padding='same')(X)
    X = BatchNormalization()(X)
    X = ReLU()(X)

    # Second component of main path
    X = Conv2D(filters=F2, kernel_size=(3, 3), strides=(1, 1), padding='same')(X)
    X = BatchNormalization()(X)

    # Add shortcut value
    X = Add()([X, X_shortcut])
    X = ReLU()(X)

    return X

# Convolutional Block with downsampling (used in ResNet)
def conv_block(X, f, filters, s=2):
    F1, F2 = filters

    # Save the input value for shortcut
    X_shortcut = X

    # First component of main path
    X = Conv2D(F1, (3, 3), strides=(s, s), padding='same')(X)
    X = BatchNormalization()(X)
    X = ReLU()(X)

    # Second component of main path
    X = Conv2D(F2, (3, 3), strides=(1, 1), padding='same')(X)
    X = BatchNormalization()(X)

    # Shortcut path
    X_shortcut = Conv2D(F2, (1, 1), strides=(s, s))(X_shortcut)
    X_shortcut = BatchNormalization()(X_shortcut)

    # Add shortcut to main path
    X = Add()([X, X_shortcut])
    X = ReLU()(X)

    return X

# Build ResNet18 model
def ResNet18(input_shape, gender_input_shape, classes=1000):
    # Define the input tensor
    X_input = Input(input_shape)
    gender_input = Input(gender_input_shape)

    # Stage 1 (Initial Conv Layer)
    X = Conv2D(64, (7, 7), strides=(2, 2), padding='same')(X_input)
    X = BatchNormalization()(X)
    X = ReLU()(X)
    X = MaxPooling2D((3, 3), strides=(2, 2), padding='same')(X)

    # Stage 2
    X = conv_block(X, f=3, filters=[64, 64], s=1)
    X = identity_block(X, f=3, filters=[64, 64])

    # Stage 3
    X = conv_block(X, f=3, filters=[128, 128], s=2)
    X = identity_block(X, f=3, filters=[128, 128])

    # Stage 4
    X = conv_block(X, f=3, filters=[256, 256], s=2)
    X = identity_block(X, f=3, filters=[256, 256])

    # Stage 5
    X = conv_block(X, f=3, filters=[512, 512], s=2)
    X = identity_block(X, f=3, filters=[512, 512])

    # Average Pooling
    X = GlobalAveragePooling2D()(X)

    # Fully connected layer for gender input
    gender_dense = Dense(16, activation='relu')(gender_input)

    # Concatenate gender input with the main output
    X = Concatenate()([X, gender_dense])
   
    # Output layer (fully connected)
    if isinstance(classes, int):
        if classes == 1:
            X = Dense(classes, activation='sigmoid')(X)
        else:
            X = Dense(classes, activation='softmax')(X)
    else:
        X = Dense(1, activation='linear')(X)

     # Create model
    model = Model(inputs=[X_input, gender_input], outputs = X, name='ResNet18')

    return model

def ResNet18_CBAM(input_shape, gender_input_shape, classes=1000):
    # Define the input tensor
    X_input = Input(input_shape)
    gender_input = Input(gender_input_shape)

    # Stage 1 (Initial Conv Layer)
    X = Conv2D(64, (7, 7), strides=(2, 2), padding='same')(X_input)
    X = BatchNormalization()(X)
    X = ReLU()(X)
    X = MaxPooling2D((3, 3), strides=(2, 2), padding='same')(X)

    # Add CBAM module
    X = cbam_block(X)

    # Stage 2
    X = conv_block(X, f=3, filters=[64, 64], s=1)
    X = identity_block(X, f=3, filters=[64, 64])

    # Add CBAM module
    X = cbam_block(X)

    # Stage 3
    X = conv_block(X, f=3, filters=[128, 128], s=2)
    X = identity_block(X, f=3, filters=[128, 128])
    
    # Add CBAM module
    X = cbam_block(X)

    # Stage 4
    X = conv_block(X, f=3, filters=[256, 256], s=2)
    X = identity_block(X, f=3, filters=[256, 256])
    
    # Add CBAM module
    X = cbam_block(X)

    # Stage 5
    X = conv_block(X, f=3, filters=[512, 512], s=2)
    X = identity_block(X, f=3, filters=[512, 512])

    # Average Pooling
    X = GlobalAveragePooling2D()(X)

    # Fully connected layer for gender input
    gender_dense = Dense(16, activation='relu')(gender_input)

    # Concatenate gender input with the main output
    X = Concatenate()([X, gender_dense])

    # Output layer (fully connected)
    if isinstance(classes, int):
        if classes == 1:
            X = Dense(classes, activation='sigmoid')(X)
        else:
            X = Dense(classes, activation='softmax')(X)
    else:
        X = Dense(1, activation='linear')(X)

    # Create model
    model = Model(inputs=[X_input, gender_input], outputs=X, name='ResNet18_CBAM')

    return model


if __name__ == "__main__":
    # Create the ResNet18 model
    model = ResNet18_CBAM(input_shape=(224, 224, 3), classes='regression')

    # Compile the model
    model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['mean_absolute_error'])

    # Print the model summary
    model.summary()
