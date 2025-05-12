import tensorflow as tf
import os
import shutil
import tempfile

def load_dataset_generic(config, data_dir, class_dirs):
    """
    Generic dataset loader that can be used for most medical image datasets
    
    Args:
        config: Configuration dictionary
        data_dir: Base directory for the dataset
        class_dirs: Dictionary mapping class names to their subdirectories
        
    Returns:
        Dictionary with train and validation datasets
    """
    img_size = tuple(config['model']['input_shape'][:2])
    batch_size = config['training']['batch_size']
    
    # Create a temporary directory with class subfolders for tf.keras.preprocessing
    temp_root = tempfile.mkdtemp()
    
    try:
        # Copy files to temp directory with class structure
        for class_name, src_dir in class_dirs.items():
            full_src_dir = os.path.join(data_dir, src_dir)
            if not os.path.exists(full_src_dir):
                raise ValueError(f"Source directory not found: {full_src_dir}")
                
            dst_dir = os.path.join(temp_root, class_name)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
                
            for fname in os.listdir(full_src_dir):
                if fname.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')):
                    src = os.path.join(full_src_dir, fname)
                    dst = os.path.join(dst_dir, fname)
                    if not os.path.exists(dst):
                        shutil.copy2(src, dst)
        
        # Use a validation split
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            temp_root, 
            image_size=img_size, 
            batch_size=batch_size, 
            label_mode='categorical',
            validation_split=0.2, 
            subset='training', 
            seed=42
        )
        
        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            temp_root, 
            image_size=img_size, 
            batch_size=batch_size, 
            label_mode='categorical',
            validation_split=0.2, 
            subset='validation', 
            seed=42
        )
        
        # Apply data augmentation to training set
        data_augmentation = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
        ])
        
        train_ds = train_ds.map(
            lambda x, y: (data_augmentation(x, training=True), y),
            num_parallel_calls=tf.data.AUTOTUNE
        )
        
        # Use buffered prefetching
        train_ds = train_ds.prefetch(buffer_size=tf.data.AUTOTUNE)
        val_ds = val_ds.prefetch(buffer_size=tf.data.AUTOTUNE)
        
        return {'train': train_ds, 'val': val_ds}
        
    except Exception as e:
        # Clean up temp directory in case of error
        shutil.rmtree(temp_root, ignore_errors=True)
        raise e
