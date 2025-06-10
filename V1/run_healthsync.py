#!/usr/bin/env python3
"""
HealthSync Application Startup Script
Initializes and runs the complete HealthSync platform
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating necessary directories...")
    directories = [
        "uploads",
        "models", 
        "data",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created/verified directory: {directory}")

def initialize_database():
    """Initialize the blood bank database"""
    print("\n🗄️ Initializing database...")
    try:
        from blood_bank.models import init_db
        db_session = init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def download_sample_data():
    """Download or create sample medical imaging data"""
    print("\n📊 Setting up sample data...")
    
    # Create sample dataset structure
    datasets = [
        "chest_xray",
        "brain_mri", 
        "isic",
        "covid19_xray",
        "blood_cells"
    ]
    
    for dataset in datasets:
        dataset_path = Path(f"data/{dataset}")
        dataset_path.mkdir(exist_ok=True)
        
        # Create train/test directories
        (dataset_path / "train").mkdir(exist_ok=True)
        (dataset_path / "test").mkdir(exist_ok=True)
        
        print(f"✅ Created dataset structure for {dataset}")
    
    print("ℹ️  Note: Add your medical imaging datasets to the data/ directory")
    print("ℹ️  Each dataset should have train/ and test/ subdirectories")

def check_config():
    """Check if configuration file exists"""
    print("\n⚙️ Checking configuration...")
    
    if not os.path.exists("config.yaml"):
        print("📝 Creating default configuration file...")
        default_config = """
# HealthSync Configuration
model:
  name: "resnet50"
  input_shape: [224, 224, 3]
  num_classes: 2

training:
  batch_size: 32
  epochs: 10
  learning_rate: 0.001

data:
  validation_split: 0.2
  test_split: 0.1

server:
  host: "0.0.0.0"
  port: 5000
  debug: true
"""
        with open("config.yaml", "w") as f:
            f.write(default_config)
        print("✅ Configuration file created")
    else:
        print("✅ Configuration file exists")

def run_tests():
    """Run system tests"""
    print("\n🧪 Running system tests...")
    try:
        subprocess.run([sys.executable, "test_system.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Some tests failed, but the system may still work")
        return False

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting HealthSync application...")
    print("=" * 50)
    print("🏥 HealthSync - Integrated Healthcare Platform")
    print("=" * 50)
    print(f"🌐 Web Interface: http://localhost:5000")
    print(f"🔬 Medical Imaging: http://localhost:5000/medical-imaging")
    print(f"🩸 Blood Bank: http://localhost:5000/blood-bank")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:5000")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 HealthSync application stopped")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")

def main():
    """Main startup function"""
    print("🏥 HealthSync Platform Startup")
    print("=" * 40)
    
    # Check system requirements
    if not check_python_version():
        return
    
    # Setup steps
    steps = [
        ("Installing packages", install_requirements),
        ("Creating directories", create_directories),
        ("Checking configuration", check_config),
        ("Initializing database", initialize_database),
        ("Setting up sample data", download_sample_data)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ Failed at step: {step_name}")
            print("Please fix the errors above and try again")
            return
    
    print("\n✅ All setup steps completed successfully!")
    
    # Ask user if they want to run tests
    response = input("\n🧪 Run system tests? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        run_tests()
    
    # Ask user if they want to start the application
    response = input("\n🚀 Start HealthSync application? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        start_application()
    else:
        print("\n📝 To start the application later, run:")
        print("   python app.py")
        print("\n📝 To run tests, run:")
        print("   python test_system.py")

if __name__ == "__main__":
    main()
