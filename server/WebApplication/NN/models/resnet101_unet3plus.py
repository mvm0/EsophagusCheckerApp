from keras.applications.resnet import ResNet101
from keras.layers import *
from keras.models import *


def aggregate(l1, l2, l3, l4, l5):
    out = concatenate([l1, l2, l3, l4, l5], axis=-1)
    out = Conv2D(320, 3, activation='relu', padding='same')(out)
    out = BatchNormalization()(out)
    out = ReLU()(out)
    return out


# ResNet101 U-Net3+
def resnet101_encoder_unet3plus(input_shape=(256, 256, 3), num_classes=1):
    resnet101_model = ResNet101(input_shape=input_shape, weights=None, include_top=False)

    XE5 = resnet101_model.get_layer('conv4_block23_out').output
    XE5 = Conv2D(1024, 3, activation='relu', padding='same')(XE5)
    XE5 = Conv2D(1024, 3, activation='relu', padding='same')(XE5)
    XE5 = Dropout(0.5)(XE5)

    XD4_from_XE5 = Conv2D(64, 3, activation='relu', padding='same')(
        UpSampling2D(size=(2, 2), interpolation='bilinear')(XE5))
    XD4_from_XE4 = Conv2D(64, 3, activation='relu', padding='same')(
        resnet101_model.get_layer('conv3_block4_out').output)
    XD4_from_XE3 = Conv2D(64, 3, activation='relu', padding='same')(
        MaxPooling2D(pool_size=(2, 2))(resnet101_model.get_layer('conv2_block3_out').output))
    XD4_from_XE2 = Conv2D(64, 3, activation='relu', padding='same')(
        MaxPooling2D(pool_size=(4, 4))(resnet101_model.get_layer('conv1_relu').output))
    XD4_from_XE1 = Conv2D(64, 3, activation='relu', padding='same')(
        MaxPooling2D(pool_size=(8, 8))(resnet101_model.get_layer(index=0).output))
    XD4 = aggregate(XD4_from_XE5, XD4_from_XE4, XD4_from_XE3, XD4_from_XE2, XD4_from_XE1)

    XD3_from_XE5 = Conv2D(64, 3, activation='relu', padding='same')(
        UpSampling2D(size=(4, 4), interpolation='bilinear')(XE5))
    XD3_from_XD4 = Conv2D(64, 3, activation='relu', padding='same')(
        UpSampling2D(size=(2, 2), interpolation='bilinear')(XD4))
    XD3_from_XE3 = Conv2D(64, 3, activation='relu', padding='same')(
        resnet101_model.get_layer('conv2_block3_out').output)
    XD3_from_XE2 = Conv2D(64, 3, activation='relu', padding='same')(
        MaxPooling2D(pool_size=(2, 2))(resnet101_model.get_layer('conv1_relu').output))
    XD3_from_XE1 = Conv2D(64, 3, activation='relu', padding='same')(
        MaxPooling2D(pool_size=(4, 4))(resnet101_model.get_layer(index=0).output))
    XD3 = aggregate(XD3_from_XE5, XD3_from_XD4, XD3_from_XE3, XD3_from_XE2, XD3_from_XE1)

    XD2_from_XE5 = Conv2D(64, 3, activation='relu', padding='same')(
        UpSampling2D(size=(8, 8), interpolation='bilinear')(XE5))
    XD2_from_XD4 = Conv2D(64, 3, activation='relu', padding='same')(
        UpSampling2D(size=(4, 4), interpolation='bilinear')(XD4))
    XD2_from_XD3 = Conv2D(64, 3, activation='relu', padding='same')(
        UpSampling2D(size=(2, 2), interpolation='bilinear')(XD3))
    XD2_from_XE2 = Conv2D(64, 3, activation='relu', padding='same')(resnet101_model.get_layer('conv1_relu').output)
    XD2_from_XE1 = Conv2D(64, 3, activation='relu', padding='same')(
        MaxPooling2D(pool_size=(2, 2))(resnet101_model.get_layer(index=0).output))
    XD2 = aggregate(XD2_from_XE5, XD2_from_XD4, XD2_from_XD3, XD2_from_XE2, XD2_from_XE1)

    XD1_from_XE5 = Conv2D(64, 3, activation='relu', padding='same')(
        UpSampling2D(size=(16, 16), interpolation='bilinear')(XE5))
    XD1_from_XD4 = Conv2D(64, 3, activation='relu', padding='same')(
        UpSampling2D(size=(8, 8), interpolation='bilinear')(XD4))
    XD1_from_XD3 = Conv2D(64, 3, activation='relu', padding='same')(
        UpSampling2D(size=(4, 4), interpolation='bilinear')(XD3))
    XD1_from_XD2 = Conv2D(64, 3, activation='relu', padding='same')(
        UpSampling2D(size=(2, 2), interpolation='bilinear')(XD2))
    XD1_from_XE1 = Conv2D(64, 3, activation='relu', padding='same')(resnet101_model.get_layer(index=0).output)
    XD1 = aggregate(XD1_from_XE5, XD1_from_XD4, XD1_from_XD3, XD1_from_XD2, XD1_from_XE1)

    out = Conv2D(160, 3, activation='relu', padding='same')(XD1)
    if num_classes > 1:
        out = Conv2D(num_classes, 1, activation='softmax', padding='same')(out)
    else:
        out = Conv2D(num_classes, 1, activation='sigmoid', padding='same')(out)

    model = Model(inputs=resnet101_model.input, outputs=out)
    for layer in model.layers:
        layer.trainable = True
    return model