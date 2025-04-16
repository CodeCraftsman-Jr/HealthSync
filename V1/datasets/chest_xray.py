import tensorflow as tf
import os

def load_chest_xray(config):
    # Use the extracted TB_Chest_Radiography_Database structure
    data_dir = 'data/chest_xray/TB_Chest_Radiography_Database'
    normal_dir = os.path.join(data_dir, 'Normal')
    tb_dir = os.path.join(data_dir, 'Tuberculosis')
    img_size = tuple(config['model']['input_shape'][:2])
    batch_size = config['training']['batch_size']

    # Create a temporary directory with class subfolders for tf.keras.preprocessing
    import shutil, tempfile
    temp_root = tempfile.mkdtemp()
    class_dirs = {'Normal': normal_dir, 'Tuberculosis': tb_dir}
    for class_name, src_dir in class_dirs.items():
        dst_dir = os.path.join(temp_root, class_name)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for fname in os.listdir(src_dir):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                src = os.path.join(src_dir, fname)
                dst = os.path.join(dst_dir, fname)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)

    # Use a validation split
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        temp_root, image_size=img_size, batch_size=batch_size, label_mode='categorical', validation_split=0.2, subset='training', seed=42)
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        temp_root, image_size=img_size, batch_size=batch_size, label_mode='categorical', validation_split=0.2, subset='validation', seed=42)
    return {'train': train_ds, 'val': val_ds}
