import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import tensorflow as tf
from utils.model import get_model
from datasets.get_dataset import get_dataset
import yaml
import numpy as np
from PIL import Image
import io
import base64
from blood_bank.api import blood_bank_api
from blood_bank.models import init_db

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'healthsync_secret_key')

# Register blood bank API blueprint
app.register_blueprint(blood_bank_api, url_prefix='/api/blood-bank')

# Initialize blood bank database
blood_bank_db = init_db()

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Global variables to store loaded models
loaded_models = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/medical-imaging')
def medical_imaging():
    return render_template('medical_imaging.html')

@app.route('/blood-bank')
def blood_bank():
    return render_template('blood_bank.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/hospital-dashboard')
def hospital_dashboard():
    return render_template('hospital_dashboard.html')

@app.route('/donor-dashboard')
def donor_dashboard():
    return render_template('donor_dashboard.html')

@app.route('/api/datasets')
def get_datasets():
    """Get list of available datasets"""
    dataset_list = []
    for dataset_dir in os.listdir('data'):
        if os.path.isdir(os.path.join('data', dataset_dir)):
            dataset_list.append(dataset_dir)
    return jsonify({'datasets': dataset_list})

@app.route('/api/models')
def get_models():
    """Get list of available models"""
    return jsonify({'models': ['basic_cnn', 'resnet50', 'efficientnet']})

@app.route('/api/load-model', methods=['POST'])
def load_model():
    """Load a model for a specific dataset"""
    data = request.json
    dataset_name = data.get('dataset')
    model_name = data.get('model', 'resnet50')
    
    if not dataset_name:
        return jsonify({'error': 'Dataset name is required'}), 400
    
    # Check if model is already loaded
    if dataset_name in loaded_models:
        return jsonify({'message': f'Model for {dataset_name} already loaded'})
    
    try:
        # Update config with selected model
        model_config = config.get('model', {}).copy()
        model_config['name'] = model_name
        
        # Get dataset to determine number of classes
        dataset = get_dataset(dataset_name, config)
        if dataset:
            # Get number of classes from dataset
            for images, labels in dataset['train'].take(1):
                num_classes = labels.shape[1]
                model_config['num_classes'] = num_classes
                break
        
        # Load model
        model = get_model(model_config)
        
        # Check if weights exist and load them
        weights_path = f'models/{dataset_name}_{model_name}.h5'
        if os.path.exists(weights_path):
            model.load_weights(weights_path)
            status = 'Loaded pretrained weights'
        else:
            status = 'Initialized with random weights'
        
        # Store model in memory
        loaded_models[dataset_name] = model
        
        return jsonify({
            'message': f'Model {model_name} loaded for {dataset_name}',
            'status': status
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make a prediction on an uploaded image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    dataset_name = request.form.get('dataset')
    if not dataset_name:
        return jsonify({'error': 'Dataset name is required'}), 400
    
    if dataset_name not in loaded_models:
        return jsonify({'error': f'Model for {dataset_name} not loaded'}), 400
    
    try:
        # Read image
        image_file = request.files['image']
        image = Image.open(image_file)
        
        # Preprocess image
        input_shape = loaded_models[dataset_name].input_shape[1:3]
        image = image.resize(input_shape)
        image_array = tf.keras.preprocessing.image.img_to_array(image)
        image_array = tf.expand_dims(image_array, 0)  # Create batch dimension
        
        # Normalize image
        image_array = image_array / 255.0
        
        # Make prediction
        predictions = loaded_models[dataset_name].predict(image_array)
        
        # Get class names based on dataset
        class_names = get_class_names(dataset_name)
        
        # Format results
        results = []
        for i, prob in enumerate(predictions[0]):
            if i < len(class_names):
                results.append({
                    'class': class_names[i],
                    'probability': float(prob)
                })
        
        # Sort by probability
        results = sorted(results, key=lambda x: x['probability'], reverse=True)
        
        return jsonify({
            'predictions': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_class_names(dataset_name):
    """Get class names for a dataset"""
    # This is a simplified version - in a real app, you'd get this from the dataset
    if dataset_name == 'chest_xray':
        return ['Normal', 'Pneumonia']
    elif dataset_name == 'brain_mri':
        return ['No Tumor', 'Tumor']
    elif dataset_name == 'isic':
        return ['Benign', 'Malignant']
    elif dataset_name == 'covid19_xray':
        return ['COVID', 'Normal', 'Viral Pneumonia']
    elif dataset_name == 'blood_cells':
        return ['EOSINOPHIL', 'LYMPHOCYTE', 'MONOCYTE', 'NEUTROPHIL']
    else:
        # Generic positive/negative classes
        return ['Negative', 'Positive']

# Static files route for uploaded images
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Start the app
    app.run(debug=True, host='0.0.0.0', port=5000)
