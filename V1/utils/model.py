import tensorflow as tf

def get_model(model_config):
    name = model_config.get('name', 'basic_cnn')
    input_shape = tuple(model_config.get('input_shape', [224, 224, 3]))
    num_classes = model_config.get('num_classes', 2)

    if name == 'basic_cnn':
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=input_shape),
            tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
    elif name == 'resnet50':
        base = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
        base.trainable = False
        model = tf.keras.Sequential([
            base,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
    elif name == 'efficientnet':
        base = tf.keras.applications.EfficientNetB0(weights='imagenet', include_top=False, input_shape=input_shape)
        base.trainable = False
        model = tf.keras.Sequential([
            base,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
    else:
        raise ValueError(f"Unknown model: {name}")
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model
