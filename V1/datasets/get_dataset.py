import os

def get_dataset(name, config):
    if name == 'chest_xray':
        from .chest_xray import load_chest_xray
        return load_chest_xray(config)
    elif name == 'isic':
        from .isic import load_isic
        return load_isic(config)
    elif name == 'brain_mri':
        from .brain_mri import load_brain_mri
        return load_brain_mri(config)
    else:
        raise ValueError(f"Unknown dataset: {name}")
