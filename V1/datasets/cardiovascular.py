import os
from .dataset_template import load_dataset_generic

def load_heart_ecg(config):
    """
    Load Heart Disease ECG dataset
    Dataset structure: normal/abnormal
    """
    data_dir = 'data/heart_ecg'
    class_dirs = {
        'Normal': 'normal',
        'Abnormal': 'abnormal'
    }
    return load_dataset_generic(config, data_dir, class_dirs)

def load_coronary_artery(config):
    """
    Load Coronary Artery Disease dataset
    Dataset structure: positive/negative
    """
    data_dir = 'data/coronary_artery'
    class_dirs = {
        'Positive': 'positive',
        'Negative': 'negative'
    }
    return load_dataset_generic(config, data_dir, class_dirs)

def load_cardiac_mri(config):
    """
    Load Cardiac MRI dataset
    Dataset structure: normal/abnormal
    """
    data_dir = 'data/cardiac_mri'
    class_dirs = {
        'Normal': 'normal',
        'Abnormal': 'abnormal'
    }
    return load_dataset_generic(config, data_dir, class_dirs)
