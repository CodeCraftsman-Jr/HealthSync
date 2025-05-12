import os
from .dataset_template import load_dataset_generic

def load_blood_cells(config):
    """
    Load Blood Cell Classification dataset
    Dataset structure: EOSINOPHIL/LYMPHOCYTE/MONOCYTE/NEUTROPHIL
    """
    data_dir = 'data/blood_cells'
    class_dirs = {
        'EOSINOPHIL': 'EOSINOPHIL',
        'LYMPHOCYTE': 'LYMPHOCYTE',
        'MONOCYTE': 'MONOCYTE',
        'NEUTROPHIL': 'NEUTROPHIL'
    }
    return load_dataset_generic(config, data_dir, class_dirs)

def load_leukemia(config):
    """
    Load Leukemia Classification dataset
    Dataset structure: ALL_IDB1/ALL_IDB2
    ALL_IDB1: Acute Lymphoblastic Leukemia
    ALL_IDB2: Normal blood cells
    """
    data_dir = 'data/leukemia'
    class_dirs = {
        'Leukemia': 'ALL_IDB1',
        'Normal': 'ALL_IDB2'
    }
    return load_dataset_generic(config, data_dir, class_dirs)
