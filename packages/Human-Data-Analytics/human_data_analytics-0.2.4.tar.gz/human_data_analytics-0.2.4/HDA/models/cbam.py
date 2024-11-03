import tensorflow as tf
from tensorflow.keras.layers import Conv2D, GlobalAveragePooling2D, GlobalMaxPooling2D, Dense, Multiply, Reshape, Add, Concatenate, Activation, Layer

# Channel Attention Block
def channel_attention(input_feature, ratio=8):
    channel_axis = -1
    channel = input_feature.shape[channel_axis]
    
    shared_layer_one = Dense(channel // ratio,
                             activation='relu',
                             kernel_initializer='he_normal',
                             use_bias=True,
                             bias_initializer='zeros')
    shared_layer_two = Dense(channel,
                             kernel_initializer='he_normal',
                             use_bias=True,
                             bias_initializer='zeros')
    
    avg_pool = GlobalAveragePooling2D()(input_feature)
    avg_pool = Reshape((1, 1, channel))(avg_pool)
    avg_pool = shared_layer_one(avg_pool)
    avg_pool = shared_layer_two(avg_pool)
    
    max_pool = GlobalMaxPooling2D()(input_feature)
    max_pool = Reshape((1, 1, channel))(max_pool)
    max_pool = shared_layer_one(max_pool)
    max_pool = shared_layer_two(max_pool)
    
    cbam_feature = Add()([avg_pool, max_pool])
    cbam_feature = Activation('sigmoid')(cbam_feature)
    
    return Multiply()([input_feature, cbam_feature])

# Spatial Attention Block using Keras layers only
class SpatialAttention(Layer):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        self.conv = Conv2D(filters=1,
                           kernel_size=kernel_size,
                           strides=1,
                           padding='same',
                           activation='sigmoid',
                           kernel_initializer='he_normal',
                           use_bias=False)
    
    def call(self, input_feature):
        avg_pool = tf.reduce_mean(input_feature, axis=-1, keepdims=True)
        max_pool = tf.reduce_max(input_feature, axis=-1, keepdims=True)
        concat = Concatenate(axis=-1)([avg_pool, max_pool])
        
        cbam_feature = self.conv(concat)  # Apply convolution
        return Multiply()([input_feature, cbam_feature])

# CBAM Block (Channel + Spatial Attention)
def cbam_block(input_feature, ratio=8):
    cbam_feature = channel_attention(input_feature, ratio)
    cbam_feature = SpatialAttention()(cbam_feature)
    return cbam_feature

if __name__ == "__main__":
    # Example usage
    input_layer = tf.keras.layers.Input(shape=(64, 64, 256))  # Example input shape
    output = cbam_block(input_layer)

    model = tf.keras.models.Model(inputs=input_layer, outputs=output)
    model.summary()
