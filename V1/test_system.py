#!/usr/bin/env python3
"""
HealthSync System Test Script
Tests the complete functionality of the HealthSync platform
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def test_medical_imaging():
    """Test medical imaging functionality"""
    print("\n=== Testing Medical Imaging System ===")
    
    # Test getting available datasets
    print("1. Testing dataset retrieval...")
    response = requests.get(f"{API_BASE}/datasets")
    if response.status_code == 200:
        datasets = response.json().get('datasets', [])
        print(f"✓ Found {len(datasets)} datasets: {datasets}")
    else:
        print(f"✗ Failed to get datasets: {response.status_code}")
        return False
    
    # Test model loading
    print("2. Testing model loading...")
    if datasets:
        test_dataset = datasets[0] if datasets else 'chest_xray'
        model_data = {
            'dataset': test_dataset,
            'model': 'resnet50'
        }
        response = requests.post(f"{API_BASE}/load-model", json=model_data)
        if response.status_code == 200:
            print(f"✓ Model loaded for {test_dataset}")
        else:
            print(f"✗ Failed to load model: {response.status_code}")
            print(response.text)
    
    print("✓ Medical imaging tests completed")
    return True

def test_blood_bank_system():
    """Test blood bank functionality"""
    print("\n=== Testing Blood Bank System ===")
    
    # Test hospital registration
    print("1. Testing hospital registration...")
    hospital_data = {
        'name': 'Test General Hospital',
        'address': '123 Medical Plaza, Test City',
        'contact_number': '+1-555-0123',
        'email': 'test@hospital.com',
        'password': 'hospital123'
    }
    
    response = requests.post(f"{API_BASE}/blood-bank/hospital/register", json=hospital_data)
    if response.status_code == 201:
        print("✓ Hospital registered successfully")
    else:
        print(f"✗ Hospital registration failed: {response.status_code}")
        print(response.text)
        return False
    
    # Test hospital login
    print("2. Testing hospital login...")
    login_data = {
        'email': hospital_data['email'],
        'password': hospital_data['password']
    }
    
    response = requests.post(f"{API_BASE}/blood-bank/hospital/login", json=login_data)
    if response.status_code == 200:
        hospital_token = response.json().get('token')
        hospital_id = response.json().get('hospital_id')
        print("✓ Hospital login successful")
    else:
        print(f"✗ Hospital login failed: {response.status_code}")
        return False
    
    # Test donor registration
    print("3. Testing donor registration...")
    donor_data = {
        'name': 'John Test Donor',
        'blood_type': 'O_POSITIVE',
        'address': '456 Donor Street, Test City',
        'contact_number': '+1-555-0456',
        'email': 'donor@test.com',
        'password': 'donor123',
        'date_of_birth': '1990-01-15'
    }
    
    response = requests.post(f"{API_BASE}/blood-bank/donor/register", json=donor_data)
    if response.status_code == 201:
        print("✓ Donor registered successfully")
    else:
        print(f"✗ Donor registration failed: {response.status_code}")
        print(response.text)
        return False
    
    # Test donor login
    print("4. Testing donor login...")
    donor_login_data = {
        'email': donor_data['email'],
        'password': donor_data['password']
    }
    
    response = requests.post(f"{API_BASE}/blood-bank/donor/login", json=donor_login_data)
    if response.status_code == 200:
        donor_token = response.json().get('token')
        donor_id = response.json().get('donor_id')
        print("✓ Donor login successful")
    else:
        print(f"✗ Donor login failed: {response.status_code}")
        return False
    
    # Test adding blood to inventory
    print("5. Testing blood inventory management...")
    headers = {'Authorization': f'Bearer {hospital_token}'}
    inventory_data = {
        'blood_type': 'O_POSITIVE',
        'quantity_ml': 450,
        'expiry_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    }
    
    response = requests.post(f"{API_BASE}/blood-bank/hospital/inventory/add", 
                           json=inventory_data, headers=headers)
    if response.status_code == 201:
        print("✓ Blood added to inventory successfully")
    else:
        print(f"✗ Failed to add blood to inventory: {response.status_code}")
        print(response.text)
    
    # Test getting inventory
    print("6. Testing inventory retrieval...")
    response = requests.get(f"{API_BASE}/blood-bank/hospital/inventory", headers=headers)
    if response.status_code == 200:
        inventory = response.json().get('inventory', [])
        print(f"✓ Retrieved inventory with {len(inventory)} items")
    else:
        print(f"✗ Failed to retrieve inventory: {response.status_code}")
    
    # Test creating blood request
    print("7. Testing blood request creation...")
    request_data = {
        'blood_type': 'A_POSITIVE',
        'quantity_ml': 900,
        'urgency_level': 4
    }
    
    response = requests.post(f"{API_BASE}/blood-bank/hospital/request", 
                           json=request_data, headers=headers)
    if response.status_code == 201:
        request_id = response.json().get('request_id')
        print("✓ Blood request created successfully")
    else:
        print(f"✗ Failed to create blood request: {response.status_code}")
        print(response.text)
    
    # Test donor profile
    print("8. Testing donor profile...")
    donor_headers = {'Authorization': f'Bearer {donor_token}'}
    response = requests.get(f"{API_BASE}/blood-bank/donor/profile", headers=donor_headers)
    if response.status_code == 200:
        profile = response.json().get('donor', {})
        print(f"✓ Retrieved donor profile for {profile.get('name')}")
    else:
        print(f"✗ Failed to retrieve donor profile: {response.status_code}")
    
    # Test recording donation
    print("9. Testing blood donation recording...")
    donation_data = {
        'hospital_id': hospital_id,
        'quantity_ml': 450
    }
    
    response = requests.post(f"{API_BASE}/blood-bank/donor/donate", 
                           json=donation_data, headers=donor_headers)
    if response.status_code == 201:
        print("✓ Blood donation recorded successfully")
    else:
        print(f"✗ Failed to record donation: {response.status_code}")
        print(response.text)
    
    # Test getting urgent requests
    print("10. Testing urgent requests...")
    response = requests.get(f"{API_BASE}/blood-bank/urgent-requests")
    if response.status_code == 200:
        urgent_requests = response.json().get('urgent_requests', [])
        print(f"✓ Retrieved {len(urgent_requests)} urgent requests")
    else:
        print(f"✗ Failed to retrieve urgent requests: {response.status_code}")
    
    print("✓ Blood bank tests completed")
    return True

def test_web_interface():
    """Test web interface accessibility"""
    print("\n=== Testing Web Interface ===")
    
    pages = [
        ('/', 'Home Page'),
        ('/medical-imaging', 'Medical Imaging'),
        ('/blood-bank', 'Blood Bank'),
        ('/login', 'Login Page'),
        ('/register', 'Registration Page'),
        ('/hospital-dashboard', 'Hospital Dashboard'),
        ('/donor-dashboard', 'Donor Dashboard')
    ]
    
    for url, name in pages:
        try:
            response = requests.get(f"{BASE_URL}{url}")
            if response.status_code == 200:
                print(f"✓ {name} accessible")
            else:
                print(f"✗ {name} failed: {response.status_code}")
        except Exception as e:
            print(f"✗ {name} error: {str(e)}")
    
    print("✓ Web interface tests completed")
    return True

def main():
    """Run all tests"""
    print("HealthSync System Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("✗ Server is not responding correctly")
            return
    except Exception as e:
        print(f"✗ Cannot connect to server at {BASE_URL}")
        print("Please make sure the Flask app is running with: python app.py")
        return
    
    print("✓ Server is running")
    
    # Run tests
    tests = [
        test_web_interface,
        test_medical_imaging,
        test_blood_bank_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with error: {str(e)}")
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! HealthSync system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the output above.")

if __name__ == "__main__":
    main()
