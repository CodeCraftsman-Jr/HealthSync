import tensorflow as tf
import os

def load_brain_mri(config):
    # Download dataset if not present (user must have Kaggle API set up)
    data_dir = 'data/brain_mri'
    if not os.path.exists(data_dir):
        print('Please download Brain MRI dataset from Kaggle and unzip to data/brain_mri')
    train_dir = os.path.join(data_dir, 'train')
    val_dir = os.path.join(data_dir, 'val')
    img_size = tuple(config['model']['input_shape'][:2])
    batch_size = config['training']['batch_size']
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        train_dir, image_size=img_size, batch_size=batch_size, label_mode='categorical')
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        val_dir, image_size=img_size, batch_size=batch_size, label_mode='categorical')
    return {'train': train_ds, 'val': val_ds}
