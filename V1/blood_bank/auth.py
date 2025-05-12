from werkzeug.security import generate_password_hash, check_password_hash
from .models import Hospital, Donor, init_db
import jwt
import datetime
import os
from functools import wraps
from flask import request, jsonify, current_app

# Initialize database session
db_session = init_db()

def generate_token(user_id, is_hospital):
    """Generate JWT token for authenticated users"""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'is_hospital': is_hospital
    }
    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY', os.environ.get('SECRET_KEY', 'dev_key')),
        algorithm='HS256'
    )

def token_required(f):
    """Decorator for routes that require token authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(
                token, 
                current_app.config.get('SECRET_KEY', os.environ.get('SECRET_KEY', 'dev_key')),
                algorithms=['HS256']
            )
            
            if data['is_hospital']:
                current_user = db_session.query(Hospital).filter_by(id=data['sub']).first()
            else:
                current_user = db_session.query(Donor).filter_by(id=data['sub']).first()
                
            if not current_user:
                return jsonify({'message': 'Invalid token!'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

def register_hospital(name, address, contact_number, email, password):
    """Register a new hospital"""
    # Check if hospital already exists
    existing_hospital = db_session.query(Hospital).filter_by(email=email).first()
    if existing_hospital:
        return {'success': False, 'message': 'Hospital with this email already exists'}
    
    # Create new hospital
    new_hospital = Hospital(
        name=name,
        address=address,
        contact_number=contact_number,
        email=email,
        password_hash=generate_password_hash(password)
    )
    
    try:
        db_session.add(new_hospital)
        db_session.commit()
        return {'success': True, 'message': 'Hospital registered successfully'}
    except Exception as e:
        db_session.rollback()
        return {'success': False, 'message': f'Error registering hospital: {str(e)}'}

def register_donor(name, blood_type, address, contact_number, email, password, date_of_birth):
    """Register a new donor"""
    # Check if donor already exists
    existing_donor = db_session.query(Donor).filter_by(email=email).first()
    if existing_donor:
        return {'success': False, 'message': 'Donor with this email already exists'}
    
    # Create new donor
    new_donor = Donor(
        name=name,
        blood_type=blood_type,
        address=address,
        contact_number=contact_number,
        email=email,
        password_hash=generate_password_hash(password),
        date_of_birth=date_of_birth
    )
    
    try:
        db_session.add(new_donor)
        db_session.commit()
        return {'success': True, 'message': 'Donor registered successfully'}
    except Exception as e:
        db_session.rollback()
        return {'success': False, 'message': f'Error registering donor: {str(e)}'}

def login_hospital(email, password):
    """Login for hospitals"""
    hospital = db_session.query(Hospital).filter_by(email=email).first()
    
    if not hospital or not check_password_hash(hospital.password_hash, password):
        return {'success': False, 'message': 'Invalid email or password'}
    
    token = generate_token(hospital.id, is_hospital=True)
    return {
        'success': True,
        'token': token,
        'hospital_id': hospital.id,
        'name': hospital.name
    }

def login_donor(email, password):
    """Login for donors"""
    donor = db_session.query(Donor).filter_by(email=email).first()
    
    if not donor or not check_password_hash(donor.password_hash, password):
        return {'success': False, 'message': 'Invalid email or password'}
    
    token = generate_token(donor.id, is_hospital=False)
    return {
        'success': True,
        'token': token,
        'donor_id': donor.id,
        'name': donor.name,
        'blood_type': donor.blood_type.value
    }
