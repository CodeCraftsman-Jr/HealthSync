#!/usr/bin/env python3
"""
Simple test to check if basic functionality works
"""

print("=== HealthSync Simple Test ===")

try:
    print("1. Testing basic imports...")
    import os
    import sys
    print("✓ Basic imports work")
    
    print("2. Testing Flask import...")
    from flask import Flask
    print("✓ Flask import works")
    
    print("3. Testing SQLAlchemy import...")
    from sqlalchemy import create_engine
    print("✓ SQLAlchemy import works")
    
    print("4. Testing blood bank models...")
    from blood_bank.models import BloodType, Hospital, Donor, init_db
    print("✓ Blood bank models import works")
    
    print("5. Testing database initialization...")
    db_session = init_db('sqlite:///test.db')
    print("✓ Database initialization works")
    
    print("6. Testing Flask app creation...")
    app = Flask(__name__)
    
    @app.route('/')
    def test_route():
        return "HealthSync Test Page"
    
    print("✓ Flask app creation works")
    
    print("\n=== All Tests Passed! ===")
    print("The HealthSync system should work correctly.")
    print("You can now run: python app.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
