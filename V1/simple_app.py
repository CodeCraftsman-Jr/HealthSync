#!/usr/bin/env python3
"""
HealthSync - Simplified Version for Quick Demo
This version works with minimal dependencies
"""

try:
    from flask import Flask, render_template, request, jsonify
    print("✓ Flask imported successfully")
except ImportError:
    print("❌ Flask not found. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, render_template, request, jsonify
    print("✓ Flask installed and imported")

import os
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'healthsync_demo_key'

# Simple in-memory storage for demo
hospitals = []
donors = []
blood_inventory = []
blood_requests = []
donations = []

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

# Simple API endpoints for demo
@app.route('/api/datasets')
def get_datasets():
    """Get available datasets"""
    datasets = [
        'chest_xray',
        'brain_mri', 
        'isic',
        'covid19_xray',
        'blood_cells'
    ]
    return jsonify({'success': True, 'datasets': datasets})

@app.route('/api/models')
def get_models():
    """Get available models"""
    models = ['basic_cnn', 'resnet50', 'efficientnet']
    return jsonify({'success': True, 'models': models})

@app.route('/api/load-model', methods=['POST'])
def load_model():
    """Simulate model loading"""
    data = request.get_json()
    dataset = data.get('dataset')
    model = data.get('model', 'resnet50')
    
    return jsonify({
        'success': True,
        'message': f'Model {model} loaded for dataset {dataset}',
        'status': 'Demo mode - model simulation'
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Simulate image prediction"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image provided'}), 400
    
    dataset = request.form.get('dataset', 'chest_xray')
    
    # Simulate predictions based on dataset
    if dataset == 'chest_xray':
        predictions = [
            {'class': 'Normal', 'probability': 0.75},
            {'class': 'Pneumonia', 'probability': 0.25}
        ]
    elif dataset == 'brain_mri':
        predictions = [
            {'class': 'No Tumor', 'probability': 0.60},
            {'class': 'Tumor', 'probability': 0.40}
        ]
    else:
        predictions = [
            {'class': 'Negative', 'probability': 0.65},
            {'class': 'Positive', 'probability': 0.35}
        ]
    
    return jsonify({
        'success': True,
        'predictions': predictions,
        'note': 'This is a demo simulation'
    })

# Blood Bank API endpoints
@app.route('/api/blood-bank/register-hospital', methods=['POST'])
def register_hospital():
    """Register a new hospital"""
    data = request.get_json()
    
    hospital = {
        'id': len(hospitals) + 1,
        'name': data.get('name'),
        'email': data.get('email'),
        'address': data.get('address'),
        'contact_number': data.get('contact_number'),
        'registration_date': datetime.now().isoformat()
    }
    
    hospitals.append(hospital)
    
    return jsonify({
        'success': True,
        'message': 'Hospital registered successfully',
        'hospital_id': hospital['id'],
        'token': f'demo_token_hospital_{hospital["id"]}'
    })

@app.route('/api/blood-bank/register-donor', methods=['POST'])
def register_donor():
    """Register a new donor"""
    data = request.get_json()
    
    donor = {
        'id': len(donors) + 1,
        'name': data.get('name'),
        'email': data.get('email'),
        'blood_type': data.get('blood_type'),
        'address': data.get('address'),
        'contact_number': data.get('contact_number'),
        'date_of_birth': data.get('date_of_birth'),
        'registration_date': datetime.now().isoformat()
    }
    
    donors.append(donor)
    
    return jsonify({
        'success': True,
        'message': 'Donor registered successfully',
        'donor_id': donor['id'],
        'token': f'demo_token_donor_{donor["id"]}'
    })

@app.route('/api/blood-bank/login-hospital', methods=['POST'])
def login_hospital():
    """Hospital login"""
    data = request.get_json()
    email = data.get('email')
    
    # Find hospital by email
    hospital = next((h for h in hospitals if h['email'] == email), None)
    
    if hospital:
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'hospital_id': hospital['id'],
            'token': f'demo_token_hospital_{hospital["id"]}'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Hospital not found. Please register first.'
        }), 401

@app.route('/api/blood-bank/login-donor', methods=['POST'])
def login_donor():
    """Donor login"""
    data = request.get_json()
    email = data.get('email')
    
    # Find donor by email
    donor = next((d for d in donors if d['email'] == email), None)
    
    if donor:
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'donor_id': donor['id'],
            'token': f'demo_token_donor_{donor["id"]}'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Donor not found. Please register first.'
        }), 401

@app.route('/api/blood-bank/hospitals')
def get_hospitals():
    """Get list of hospitals"""
    return jsonify({
        'success': True,
        'hospitals': [
            {'id': h['id'], 'name': h['name'], 'address': h['address']}
            for h in hospitals
        ]
    })

@app.route('/api/blood-bank/urgent-requests')
def get_urgent_requests():
    """Get urgent blood requests"""
    urgent = [
        {
            'id': 1,
            'hospital_name': 'City General Hospital',
            'blood_type': 'O+',
            'quantity_ml': 900,
            'urgency_level': 5,
            'request_date': datetime.now().isoformat()
        },
        {
            'id': 2,
            'hospital_name': 'Regional Medical Center',
            'blood_type': 'A-',
            'quantity_ml': 450,
            'urgency_level': 4,
            'request_date': datetime.now().isoformat()
        }
    ]
    
    return jsonify({
        'success': True,
        'urgent_requests': urgent
    })

if __name__ == '__main__':
    print("🏥 HealthSync - Simplified Demo Version")
    print("=" * 50)
    print("🌐 Web Interface: http://localhost:5000")
    print("🔬 Medical Imaging: http://localhost:5000/medical-imaging")
    print("🩸 Blood Bank: http://localhost:5000/blood-bank")
    print("=" * 50)
    print("Note: This is a simplified demo version")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
