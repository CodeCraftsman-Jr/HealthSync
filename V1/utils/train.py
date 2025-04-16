def train_model(model, dataset, training_config):
    train_ds, val_ds = dataset['train'], dataset['val']
    epochs = training_config.get('epochs', 10)
    batch_size = training_config.get('batch_size', 32)

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        batch_size=batch_size
    )
    model.save('output_model.h5')
