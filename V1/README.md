# Medical Image Classifier

A flexible deep learning framework for disease detection from medical images (X-rays, MRIs, skin lesions, etc.) with Grad-CAM explainability. Easily switch between popular Kaggle datasets or add your own.

## Features
- Supports multiple datasets: Chest X-ray, ISIC skin lesion, MRI, and more
- Modular data loading and preprocessing
- TensorFlow/Keras CNN models
- Grad-CAM for explainability
- Scripts for training, evaluation, and visualization

## Usage
1. Set up your Kaggle API credentials for dataset download.
2. Configure the dataset in `config.yaml`.
3. Run `python train.py` to train the model.
4. Use `python grad_cam.py` to visualize predictions.

## Requirements
See `requirements.txt`.
