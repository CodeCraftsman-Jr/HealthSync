# HealthSync: Integrated Healthcare Platform

HealthSync is a comprehensive healthcare platform that combines AI-powered medical imaging analysis with efficient blood bank management. The system provides healthcare professionals with tools for accurate disease detection and optimal blood resource allocation.

## 🌟 Features

### 🔬 Medical Imaging Analysis
- **AI-Powered Diagnostics**: Advanced machine learning models for medical image analysis
- **50+ Medical Conditions**: Support for respiratory, neurological, dermatological, cardiovascular, and other conditions
- **Multiple AI Models**: Choose from ResNet50, EfficientNet, or Basic CNN models
- **Real-time Processing**: Fast image analysis with confidence scoring
- **Multiple Modalities**: Support for X-ray, MRI, CT, ultrasound, and other imaging types
- **Visualization**: Clear result presentation with probability scores

### 🩸 Blood Bank Management
- **Real-time Inventory**: Live tracking of blood units by type and expiry date
- **Donor Management**: Complete donor registration, scheduling, and history tracking
- **Hospital Network**: Inter-hospital blood sharing and request fulfillment
- **Emergency Alerts**: Automatic notifications for urgent blood needs
- **Smart Matching**: Intelligent blood type compatibility checking
- **Expiry Management**: Automated alerts for expiring blood units

### 👥 User Interfaces
- **Hospital Dashboard**: Comprehensive inventory and request management
- **Donor Portal**: Easy donation scheduling and history tracking
- **Medical Imaging Interface**: Intuitive image upload and analysis
- **Authentication System**: Secure login for hospitals and donors
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask 2.0+
- **AI/ML**: TensorFlow 2.8+, Keras, scikit-learn
- **Database**: SQLAlchemy, SQLite (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Bootstrap 5
- **Authentication**: JWT tokens, bcrypt password hashing
- **Image Processing**: PIL, OpenCV, NumPy
- **API**: RESTful APIs with JSON responses

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd HealthSync/V1

# Run the automated setup script
python run_healthsync.py
```

### Option 2: Manual Setup
```bash
# Clone the repository
git clone <repository-url>
cd HealthSync/V1

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads models data logs

# Initialize database
python -c "from blood_bank.models import init_db; init_db()"

# Run the application
python app.py
```

### 🌐 Access the Application
- **Main Interface**: http://localhost:5000
- **Medical Imaging**: http://localhost:5000/medical-imaging
- **Blood Bank**: http://localhost:5000/blood-bank
- **Login**: http://localhost:5000/login

## 📖 Usage Guide

### Medical Imaging Analysis
1. **Navigate** to the Medical Imaging section
2. **Select** a medical condition category from the available options
3. **Choose** an AI model (ResNet50 recommended for best accuracy)
4. **Upload** your medical image (JPEG, PNG, or DICOM format)
5. **Analyze** and view results with confidence scores
6. **Interpret** results (Note: This is for informational purposes only)

### Blood Bank Management

#### For Hospitals:
1. **Register** your hospital with contact details
2. **Login** to access the hospital dashboard
3. **Manage Inventory**: Add blood units, track expiry dates
4. **Create Requests**: Submit blood requests with urgency levels
5. **View Analytics**: Monitor donation trends and inventory status

#### For Donors:
1. **Register** with your blood type and contact information
2. **Login** to access the donor portal
3. **Schedule Donations**: Book appointments at nearby hospitals
4. **Track History**: View your donation history and impact
5. **Respond to Alerts**: Get notified about urgent blood needs

## 🔧 Configuration

### Environment Variables
```bash
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="sqlite:///healthsync.db"  # or PostgreSQL URL for production
export FLASK_ENV="development"  # or "production"
```

### Configuration File (config.yaml)
```yaml
model:
  name: "resnet50"
  input_shape: [224, 224, 3]
  num_classes: 2

training:
  batch_size: 32
  epochs: 10
  learning_rate: 0.001

server:
  host: "0.0.0.0"
  port: 5000
  debug: true
```

## 📊 Dataset Setup

### Medical Imaging Datasets
Create the following directory structure in the `data/` folder:

```
data/
├── chest_xray/
│   ├── train/
│   └── test/
├── brain_mri/
│   ├── train/
│   └── test/
├── isic/
│   ├── train/
│   └── test/
├── covid19_xray/
│   ├── train/
│   └── test/
└── blood_cells/
    ├── train/
    └── test/
```

### Supported Datasets
- **Chest X-ray**: Pneumonia detection
- **Brain MRI**: Tumor detection
- **ISIC**: Skin lesion classification
- **COVID-19 X-ray**: COVID-19 detection
- **Blood Cells**: Blood cell classification

## 🧪 Testing

### Run System Tests
```bash
# Run comprehensive system tests
python test_system.py

# Test specific components
python -m pytest tests/
```

### Manual Testing
1. **Web Interface**: Verify all pages load correctly
2. **Medical Imaging**: Upload test images and verify analysis
3. **Blood Bank**: Test registration, login, and core functionality
4. **API Endpoints**: Use tools like Postman to test API responses

## 📚 API Documentation

### Medical Imaging Endpoints
- `GET /api/datasets` - Get available medical datasets
- `GET /api/models` - Get available AI models
- `POST /api/load-model` - Load AI model for analysis
- `POST /api/predict` - Analyze uploaded medical image

### Blood Bank Endpoints

#### Authentication
- `POST /api/blood-bank/hospital/register` - Register hospital
- `POST /api/blood-bank/donor/register` - Register donor
- `POST /api/blood-bank/hospital/login` - Hospital login
- `POST /api/blood-bank/donor/login` - Donor login

#### Hospital Operations
- `GET /api/blood-bank/hospital/inventory` - Get blood inventory
- `POST /api/blood-bank/hospital/inventory/add` - Add blood to inventory
- `POST /api/blood-bank/hospital/request` - Create blood request
- `GET /api/blood-bank/hospital/requests` - Get hospital requests
- `POST /api/blood-bank/hospital/request/fulfill/{id}` - Fulfill blood request

#### Donor Operations
- `GET /api/blood-bank/donor/profile` - Get donor profile
- `POST /api/blood-bank/donor/donate` - Record blood donation
- `GET /api/blood-bank/donor/history` - Get donation history

#### Public Endpoints
- `GET /api/blood-bank/hospitals` - Get list of hospitals
- `GET /api/blood-bank/blood-types` - Get available blood types
- `GET /api/blood-bank/urgent-requests` - Get urgent blood requests

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **Role-based Access**: Different permissions for hospitals and donors
- **Input Validation**: Comprehensive data validation and sanitization
- **CORS Protection**: Cross-origin request security
- **SQL Injection Prevention**: Parameterized queries with SQLAlchemy

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production (using Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation for API changes
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TensorFlow Team** for the machine learning framework
- **Flask Team** for the web framework
- **Bootstrap Team** for the UI components
- **Medical Imaging Community** for datasets and research
- **Blood Bank Organizations** for domain expertise

## 📞 Support

For questions, issues, or support:

- **Email**: support@healthsync.com
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] Real-time notifications via WebSocket
- [ ] Mobile application (React Native)
- [ ] Advanced analytics and reporting
- [ ] Integration with hospital management systems
- [ ] Multi-language support
- [ ] Advanced AI models with federated learning
- [ ] Blockchain for blood traceability

### Version 1.1 (In Progress)
- [x] Complete blood bank management system
- [x] Medical imaging analysis
- [x] User authentication and authorization
- [x] Responsive web interface
- [ ] Email notifications
- [ ] Advanced search and filtering
- [ ] Data export functionality

---

**HealthSync** - Revolutionizing healthcare through integrated AI diagnostics and blood bank management.

*Built with ❤️ for healthcare professionals and patients worldwide.*
