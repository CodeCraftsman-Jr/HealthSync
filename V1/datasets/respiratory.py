import os
from .dataset_template import load_dataset_generic

def load_covid19_xray(config):
    """
    Load COVID-19 X-ray dataset
    Dataset structure: COVID/Normal/Viral Pneumonia
    """
    data_dir = 'data/covid19_xray'
    class_dirs = {
        'COVID': 'COVID',
        'Normal': 'Normal',
        'Viral_Pneumonia': 'Viral Pneumonia'
    }
    return load_dataset_generic(config, data_dir, class_dirs)

def load_tb_xray(config):
    """
    Load Tuberculosis X-ray dataset
    Dataset structure: Tuberculosis/Normal
    """
    data_dir = 'data/tb_xray'
    class_dirs = {
        'Tuberculosis': 'Tuberculosis',
        'Normal': 'Normal'
    }
    return load_dataset_generic(config, data_dir, class_dirs)

def load_lung_cancer_ct(config):
    """
    Load Lung Cancer CT dataset
    Dataset structure: cancer/non-cancer
    """
    data_dir = 'data/lung_cancer_ct'
    class_dirs = {
        'Cancer': 'cancer',
        'Non_Cancer': 'non-cancer'
    }
    return load_dataset_generic(config, data_dir, class_dirs)
