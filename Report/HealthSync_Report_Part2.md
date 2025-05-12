## 6. System Design

### Architecture Diagram

The HealthSync system follows a modular, layered architecture that separates concerns while enabling integration between components. The high-level architecture is illustrated below:

```
+---------------------------------------------+
|                 Client Layer                 |
|  +-------------+  +-------------+  +------+  |
|  | Web Browser |  | Mobile App  |  | API  |  |
|  +-------------+  +-------------+  +------+  |
+---------------------------------------------+
                        |
+---------------------------------------------+
|               Presentation Layer             |
|  +-------------+  +-------------+  +------+  |
|  |  Templates  |  |    Static   |  | REST |  |
|  |    (HTML)   |  |  Resources  |  | API  |  |
|  +-------------+  +-------------+  +------+  |
+---------------------------------------------+
                        |
+---------------------------------------------+
|                Business Layer                |
| +---------------+  +----------------------+  |
| | Medical Image |  | Blood Bank Management|  |
| |   Analysis    |  |        System        |  |
| +---------------+  +----------------------+  |
| +---------------+  +----------------------+  |
| | Authentication|  | Notification System  |  |
| |    System     |  |                      |  |
| +---------------+  +----------------------+  |
+---------------------------------------------+
                        |
+---------------------------------------------+
|                  Data Layer                  |
|  +-------------+  +-------------+  +------+  |
|  |   Medical   |  |    Blood    |  | User |  |
|  |   Images    |  |  Inventory  |  | Data |  |
|  +-------------+  +-------------+  +------+  |
+---------------------------------------------+
                        |
+---------------------------------------------+
|              Infrastructure Layer            |
|  +-------------+  +-------------+  +------+  |
|  |   Database  |  |  AI Model   |  | File |  |
|  |   Server    |  |   Server    |  |Storage|  |
|  +-------------+  +-------------+  +------+  |
+---------------------------------------------+
```

The architecture follows these key principles:

1. **Separation of Concerns**: Each layer has specific responsibilities, making the system easier to maintain and extend.

2. **Modularity**: Components are designed as independent modules that communicate through well-defined interfaces.

3. **Scalability**: The system can scale horizontally by adding more instances of specific components.

4. **Security**: Authentication and authorization are handled consistently across all components.

### UML Diagrams

#### Use Case Diagram

The primary actors and use cases in the HealthSync system:

```
                  +-------------------+
                  |     HealthSync    |
                  +-------------------+
                          ^
                          |
        +----------------+----------------+
        |                                 |
+---------------+                 +---------------+
| Medical Image |                 |  Blood Bank   |
|   Analysis    |                 |  Management   |
+---------------+                 +---------------+
        ^                                 ^
        |                                 |
+-------+-------+                 +-------+-------+
|               |                 |               |
|  Healthcare   |                 |   Hospital    |
| Professional  |                 | Administrator |
+---------------+                 +---------------+
        |                                 |
        |                                 |
        v                                 v
+---------------+                 +---------------+
| Upload Images |                 | Manage Blood  |
|               |                 |  Inventory    |
+---------------+                 +---------------+
        |                                 |
        v                                 v
+---------------+                 +---------------+
| View Analysis |                 | Handle Blood  |
|   Results     |                 |   Requests    |
+---------------+                 +---------------+
                                          |
                                          v
                                  +---------------+
                                  |  Donor        |
                                  +---------------+
                                          |
                                          v
                                  +---------------+
                                  | Donate Blood  |
                                  |               |
                                  +---------------+
                                          |
                                          v
                                  +---------------+
                                  | View Donation |
                                  |   History     |
                                  +---------------+
```

#### Class Diagram

Key classes in the HealthSync system:

```
+-------------------+          +-------------------+
|      User         |          |     Hospital      |
+-------------------+          +-------------------+
| id: int           |          | id: int           |
| name: string      |<>--------| name: string      |
| email: string     |          | address: string   |
| password: string  |          | contact: string   |
| role: enum        |          | email: string     |
+-------------------+          +-------------------+
        ^                              |
        |                              |
+-------+-------+                      |
|               |                      |
+-------+       +-------+              |
| Donor |       | Staff |              |
+-------+       +-------+              |
| bloodType     |                      |
| lastDonation  |                      |
| eligibility   |                      |
+---------------+                      |
        |                              |
        |                              |
        v                              v
+-------------------+          +-------------------+
|  BloodDonation    |          |  BloodInventory   |
+-------------------+          +-------------------+
| id: int           |          | id: int           |
| donorId: int      |          | hospitalId: int   |
| hospitalId: int   |          | bloodType: enum   |
| bloodType: enum   |          | quantity: float   |
| quantity: float   |          | expiryDate: date  |
| donationDate: date|          | isAvailable: bool |
+-------------------+          +-------------------+
                                      |
                                      |
                                      v
+-------------------+          +-------------------+
|   BloodRequest    |          |   Notification    |
+-------------------+          +-------------------+
| id: int           |          | id: int           |
| hospitalId: int   |          | recipientEmail    |
| bloodType: enum   |          | subject: string   |
| quantity: float   |          | message: string   |
| urgencyLevel: int |--------->| isSent: bool      |
| requestDate: date |          | createdDate: date |
| status: string    |          | sentDate: date    |
+-------------------+          +-------------------+

+-------------------+
|    ImageAnalysis  |
+-------------------+
| id: int           |
| userId: int       |
| imagePath: string |
| datasetName: string
| modelName: string |
| results: json     |
| createdDate: date |
+-------------------+
```

#### Sequence Diagram

Sequence for medical image analysis:

```
+-------------+   +-------------+   +-------------+   +-------------+
|    User     |   |    Web UI   |   |  API Server |   |  AI Model   |
+-------------+   +-------------+   +-------------+   +-------------+
       |                |                 |                 |
       | Upload Image   |                 |                 |
       |--------------->|                 |                 |
       |                | Process Upload  |                 |
       |                |---------------->|                 |
       |                |                 | Load Model      |
       |                |                 |---------------->|
       |                |                 |                 |
       |                |                 | Preprocess Image|
       |                |                 |---------------->|
       |                |                 |                 |
       |                |                 | Run Inference   |
       |                |                 |---------------->|
       |                |                 |                 |
       |                |                 | Return Results  |
       |                |                 |<----------------|
       |                |                 |                 |
       |                | Return Analysis |                 |
       |                |<----------------|                 |
       |                |                 |                 |
       | View Results   |                 |                 |
       |<---------------|                 |                 |
       |                |                 |                 |
```

Sequence for blood donation process:

```
+-------------+   +-------------+   +-------------+   +-------------+
|    Donor    |   |   Donor UI  |   |  API Server |   |  Database   |
+-------------+   +-------------+   +-------------+   +-------------+
       |                |                 |                 |
       | Login          |                 |                 |
       |--------------->|                 |                 |
       |                | Authenticate    |                 |
       |                |---------------->|                 |
       |                |                 | Verify User     |
       |                |                 |---------------->|
       |                |                 |                 |
       |                | Return Token    |                 |
       |                |<----------------|                 |
       |                |                 |                 |
       | Schedule       |                 |                 |
       | Donation       |                 |                 |
       |--------------->|                 |                 |
       |                | Create Donation |                 |
       |                |---------------->|                 |
       |                |                 | Store Donation  |
       |                |                 |---------------->|
       |                |                 |                 |
       |                |                 | Update Inventory|
       |                |                 |---------------->|
       |                |                 |                 |
       |                | Confirm         |                 |
       |                |<----------------|                 |
       |                |                 |                 |
       | View           |                 |                 |
       | Confirmation   |                 |                 |
       |<---------------|                 |                 |
       |                |                 |                 |
```

### Module Description

#### 1. Authentication Module

The Authentication Module handles user registration, login, and access control across the system. It supports multiple user roles (donors, hospital staff, administrators) with role-based permissions.

**Key Components:**
- User registration and profile management
- Secure password handling with hashing
- JWT token generation and validation
- Role-based access control
- Session management

#### 2. Medical Imaging Analysis Module

This module processes medical images and provides AI-powered analysis for various medical conditions.

**Key Components:**
- Image upload and preprocessing
- Model selection and loading
- Inference execution
- Result visualization
- Analysis history tracking

#### 3. Blood Bank Management Module

The Blood Bank Management Module handles all aspects of blood inventory, donations, and requests.

**Key Components:**
- Blood inventory tracking
- Donor management
- Donation recording
- Blood request handling
- Expiry management

#### 4. Hospital Network Module

This module enables communication and blood exchange between different hospitals in the network.

**Key Components:**
- Hospital registration and profile management
- Blood availability sharing
- Inter-hospital blood requests
- Transfer tracking

#### 5. Notification Module

The Notification Module handles alerts and communications to users based on system events.

**Key Components:**
- Email notification service
- SMS notification capability
- In-app notification management
- Notification preferences
- Scheduled reminders

#### 6. Reporting and Analytics Module

This module provides insights and reports on system usage, inventory status, and diagnostic patterns.

**Key Components:**
- Dashboard visualization
- Custom report generation
- Data export functionality
- Trend analysis
- Performance metrics

## 7. Implementation

### Tools, Languages, and Technologies Used

#### Programming Languages
- **Python 3.8**: Primary backend language
- **JavaScript (ES6+)**: Frontend interactivity
- **HTML5/CSS3**: Frontend structure and styling

#### Frameworks and Libraries
- **Flask 2.0**: Web application framework
- **SQLAlchemy 1.4**: ORM for database operations
- **TensorFlow 2.8**: Deep learning framework for medical image analysis
- **Keras**: High-level neural networks API
- **Bootstrap 5**: Frontend component library
- **jQuery**: JavaScript library for DOM manipulation
- **Chart.js**: JavaScript charting library

#### Development Tools
- **Visual Studio Code**: Primary IDE
- **Git**: Version control
- **GitHub**: Code repository
- **Docker**: Containerization
- **Postman**: API testing

#### Database
- **SQLite**: Development database
- **PostgreSQL**: Production database

#### Infrastructure
- **Nginx**: Web server
- **Gunicorn**: WSGI HTTP Server
- **Redis**: Caching and message broker

### Code Snippets

#### Medical Image Analysis Model Definition

```python
def get_model(model_config):
    name = model_config.get('name', 'basic_cnn')
    input_shape = tuple(model_config.get('input_shape', [224, 224, 3]))
    num_classes = model_config.get('num_classes', 2)

    if name == 'basic_cnn':
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=input_shape),
            tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
    elif name == 'resnet50':
        base = tf.keras.applications.ResNet50(
            weights='imagenet', 
            include_top=False, 
            input_shape=input_shape
        )
        base.trainable = False
        model = tf.keras.Sequential([
            base,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
    elif name == 'efficientnet':
        base = tf.keras.applications.EfficientNetB0(
            weights='imagenet', 
            include_top=False, 
            input_shape=input_shape
        )
        base.trainable = False
        model = tf.keras.Sequential([
            base,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
    else:
        raise ValueError(f"Unknown model: {name}")
        
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model
```

#### Blood Inventory Management

```python
def add_blood_to_inventory(hospital_id, blood_type, quantity_ml, expiry_date):
    """Add blood to hospital inventory"""
    try:
        new_inventory = BloodInventory(
            hospital_id=hospital_id,
            blood_type=blood_type,
            quantity_ml=quantity_ml,
            expiry_date=expiry_date,
            is_available=True
        )
        db_session.add(new_inventory)
        db_session.commit()
        return {'success': True, 'message': 'Blood added to inventory successfully'}
    except Exception as e:
        db_session.rollback()
        return {'success': False, 'message': f'Error adding blood to inventory: {str(e)}'}

def get_hospital_inventory(hospital_id):
    """Get blood inventory for a specific hospital"""
    try:
        inventory = db_session.query(BloodInventory).filter_by(
            hospital_id=hospital_id,
            is_available=True
        ).all()
        
        # Group by blood type
        inventory_by_type = {}
        for blood_type in BloodType:
            inventory_by_type[blood_type.value] = 0
            
        for item in inventory:
            # Skip expired blood
            if item.expiry_date < datetime.datetime.utcnow():
                item.is_available = False
                db_session.commit()
                continue
                
            inventory_by_type[item.blood_type.value] += item.quantity_ml
            
        return {
            'success': True, 
            'inventory': [
                {'blood_type': blood_type, 'quantity_ml': quantity}
                for blood_type, quantity in inventory_by_type.items()
            ]
        }
    except Exception as e:
        return {'success': False, 'message': f'Error retrieving inventory: {str(e)}'}
```

#### API Endpoint for Medical Image Analysis

```python
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
```

#### Blood Request Creation

```python
def create_blood_request(hospital_id, blood_type, quantity_ml, urgency_level):
    """Create a new blood request"""
    try:
        new_request = BloodRequest(
            hospital_id=hospital_id,
            blood_type=blood_type,
            quantity_ml=quantity_ml,
            urgency_level=urgency_level,
            status="Pending"
        )
        db_session.add(new_request)
        db_session.commit()
        
        # Check if we need to notify donors
        if urgency_level >= 4:  # High urgency
            notify_eligible_donors(blood_type)
            
        return {'success': True, 'message': 'Blood request created successfully', 'request_id': new_request.id}
    except Exception as e:
        db_session.rollback()
        return {'success': False, 'message': f'Error creating blood request: {str(e)}'}
```

### Screenshots of Output

#### Medical Imaging Analysis Interface

![Medical Imaging Analysis Interface](https://example.com/medical_imaging_interface.png)

The medical imaging analysis interface allows users to:
1. Select a medical condition category
2. Choose an AI model
3. Upload a medical image
4. View analysis results with probability scores

#### Blood Inventory Dashboard

![Blood Inventory Dashboard](https://example.com/blood_inventory_dashboard.png)

The blood inventory dashboard provides:
1. Real-time inventory levels by blood type
2. Visual indicators for critical, low, and good inventory levels
3. Expiry tracking and alerts
4. Quick actions for inventory management

#### Donor Portal

![Donor Portal](https://example.com/donor_portal.png)

The donor portal enables donors to:
1. View their donation history
2. Schedule new donations
3. Receive notifications about urgent blood needs
4. Track their eligibility status
