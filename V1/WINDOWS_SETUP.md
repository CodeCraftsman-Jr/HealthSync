# HealthSync - Windows Setup Guide

## Quick Start (Recommended)

### Option 1: Using Batch File
1. Double-click `run_healthsync.bat`
2. The script will automatically:
   - Check Python installation
   - Install required packages
   - Create necessary directories
   - Start the application

### Option 2: Using PowerShell
1. Right-click on `run_healthsync.ps1`
2. Select "Run with PowerShell"
3. If you get an execution policy error, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

## Manual Setup

### Prerequisites
1. **Python 3.8+**: Download from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation
2. **Git** (optional): For cloning the repository

### Step-by-Step Installation

1. **Open Command Prompt or PowerShell**
   ```cmd
   # Navigate to the project directory
   cd path\to\HealthSync\V1
   ```

2. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Create Directories**
   ```cmd
   mkdir uploads
   mkdir models
   mkdir data
   mkdir logs
   ```

4. **Run the Application**
   ```cmd
   python app.py
   ```

5. **Access the Application**
   - Open your web browser
   - Go to: http://localhost:5000

## Troubleshooting

### Common Issues

#### Python Not Found
- **Error**: `'python' is not recognized as an internal or external command`
- **Solution**: 
  1. Install Python from python.org
  2. Make sure "Add Python to PATH" is checked
  3. Restart Command Prompt/PowerShell

#### Permission Errors
- **Error**: PowerShell execution policy errors
- **Solution**: Run this command in PowerShell as Administrator:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

#### Package Installation Fails
- **Error**: pip install fails
- **Solution**: 
  1. Update pip: `python -m pip install --upgrade pip`
  2. Try installing packages individually
  3. Use: `pip install --user -r requirements.txt`

#### Port Already in Use
- **Error**: Port 5000 is already in use
- **Solution**: 
  1. Kill the process using port 5000
  2. Or modify `app.py` to use a different port:
     ```python
     app.run(debug=True, host='0.0.0.0', port=5001)
     ```

### Testing the Installation

1. **Test Basic Functionality**
   ```cmd
   python simple_test.py
   ```

2. **Test Web Interface**
   - Go to http://localhost:5000
   - All pages should load without errors

3. **Test API Endpoints**
   - Medical Imaging: http://localhost:5000/medical-imaging
   - Blood Bank: http://localhost:5000/blood-bank

## Features Overview

### 🔬 Medical Imaging
- Upload medical images (X-ray, MRI, CT scans)
- AI-powered analysis for 50+ medical conditions
- Multiple AI models (ResNet50, EfficientNet, Basic CNN)
- Real-time results with confidence scores

### 🩸 Blood Bank Management
- Hospital registration and login
- Donor registration and login
- Blood inventory management
- Blood request creation and fulfillment
- Donation tracking and history

### 👥 User Dashboards
- **Hospital Dashboard**: Manage inventory, create requests, view analytics
- **Donor Portal**: Schedule donations, view history, respond to urgent requests

## Next Steps

1. **Add Medical Datasets**: Place your medical imaging datasets in the `data/` folder
2. **Configure Models**: Modify `config.yaml` for your specific needs
3. **Customize Interface**: Edit templates in the `templates/` folder
4. **Deploy**: Use the deployment guide in README.md for production setup

## Support

If you encounter any issues:
1. Check this troubleshooting guide
2. Review the main README.md file
3. Check the error messages in the console
4. Ensure all dependencies are installed correctly

## Security Note

This is a development setup. For production use:
- Change the SECRET_KEY in app.py
- Use a production database (PostgreSQL)
- Enable HTTPS
- Implement proper authentication
- Follow security best practices
