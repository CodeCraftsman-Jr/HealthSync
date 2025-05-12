import os
from .dataset_template import load_dataset_generic

def load_alzheimer_mri(config):
    """
    Load Alzheimer's MRI dataset
    Dataset structure: NonDemented/VeryMildDemented/MildDemented/ModerateDemented
    """
    data_dir = 'data/alzheimer_mri'
    class_dirs = {
        'NonDemented': 'NonDemented',
        'VeryMildDemented': 'VeryMildDemented',
        'MildDemented': 'MildDemented',
        'ModerateDemented': 'ModerateDemented'
    }
    return load_dataset_generic(config, data_dir, class_dirs)

def load_stroke_ct(config):
    """
    Load Stroke CT dataset
    Dataset structure: normal/stroke
    """
    data_dir = 'data/stroke_ct'
    class_dirs = {
        'Normal': 'normal',
        'Stroke': 'stroke'
    }
    return load_dataset_generic(config, data_dir, class_dirs)

def load_parkinsons(config):
    """
    Load Parkinson's Disease dataset
    Dataset structure: healthy/parkinson
    """
    data_dir = 'data/parkinsons'
    class_dirs = {
        'Healthy': 'healthy',
        'Parkinson': 'parkinson'
    }
    return load_dataset_generic(config, data_dir, class_dirs)
