from flask import Blueprint, request, jsonify
from .auth import register_hospital, register_donor, login_hospital, login_donor, token_required
from .inventory import (add_blood_to_inventory, get_hospital_inventory, 
                       create_blood_request, fulfill_blood_request, 
                       record_blood_donation, notify_eligible_donors)
from .models import BloodType, Hospital, Donor, BloodRequest, BloodDonation, init_db
import datetime

# Initialize blueprint
blood_bank_api = Blueprint('blood_bank_api', __name__)

# Initialize database session
db_session = init_db()

# Authentication routes
@blood_bank_api.route('/hospital/register', methods=['POST'])
def api_register_hospital():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'address', 'contact_number', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    result = register_hospital(
        name=data['name'],
        address=data['address'],
        contact_number=data['contact_number'],
        email=data['email'],
        password=data['password']
    )
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@blood_bank_api.route('/donor/register', methods=['POST'])
def api_register_donor():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'blood_type', 'address', 'contact_number', 'email', 'password', 'date_of_birth']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    # Convert blood_type string to enum
    try:
        blood_type = BloodType[data['blood_type']]
    except KeyError:
        return jsonify({'success': False, 'message': 'Invalid blood type'}), 400
    
    # Convert date string to datetime
    try:
        date_of_birth = datetime.datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid date format for date_of_birth. Use YYYY-MM-DD'}), 400
    
    result = register_donor(
        name=data['name'],
        blood_type=blood_type,
        address=data['address'],
        contact_number=data['contact_number'],
        email=data['email'],
        password=data['password'],
        date_of_birth=date_of_birth
    )
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@blood_bank_api.route('/hospital/login', methods=['POST'])
def api_login_hospital():
    data = request.get_json()
    
    if 'email' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400
    
    result = login_hospital(data['email'], data['password'])
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

@blood_bank_api.route('/donor/login', methods=['POST'])
def api_login_donor():
    data = request.get_json()
    
    if 'email' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400
    
    result = login_donor(data['email'], data['password'])
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 401

# Hospital inventory routes
@blood_bank_api.route('/hospital/inventory', methods=['GET'])
@token_required
def api_get_inventory(current_user):
    # Only hospitals can access inventory
    if not isinstance(current_user, Hospital):
        return jsonify({'success': False, 'message': 'Only hospitals can access inventory'}), 403
    
    result = get_hospital_inventory(current_user.id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@blood_bank_api.route('/hospital/inventory/add', methods=['POST'])
@token_required
def api_add_inventory(current_user):
    # Only hospitals can add to inventory
    if not isinstance(current_user, Hospital):
        return jsonify({'success': False, 'message': 'Only hospitals can add to inventory'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['blood_type', 'quantity_ml', 'expiry_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    # Convert blood_type string to enum
    try:
        blood_type = BloodType[data['blood_type']]
    except KeyError:
        return jsonify({'success': False, 'message': 'Invalid blood type'}), 400
    
    # Convert date string to datetime
    try:
        expiry_date = datetime.datetime.strptime(data['expiry_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid date format for expiry_date. Use YYYY-MM-DD'}), 400
    
    result = add_blood_to_inventory(
        hospital_id=current_user.id,
        blood_type=blood_type,
        quantity_ml=data['quantity_ml'],
        expiry_date=expiry_date
    )
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

# Blood request routes
@blood_bank_api.route('/hospital/request', methods=['POST'])
@token_required
def api_create_request(current_user):
    # Only hospitals can create blood requests
    if not isinstance(current_user, Hospital):
        return jsonify({'success': False, 'message': 'Only hospitals can create blood requests'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['blood_type', 'quantity_ml', 'urgency_level']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    # Convert blood_type string to enum
    try:
        blood_type = BloodType[data['blood_type']]
    except KeyError:
        return jsonify({'success': False, 'message': 'Invalid blood type'}), 400
    
    # Validate urgency level
    if not (1 <= data['urgency_level'] <= 5):
        return jsonify({'success': False, 'message': 'Urgency level must be between 1 and 5'}), 400
    
    result = create_blood_request(
        hospital_id=current_user.id,
        blood_type=blood_type,
        quantity_ml=data['quantity_ml'],
        urgency_level=data['urgency_level']
    )
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@blood_bank_api.route('/hospital/request/fulfill/<int:request_id>', methods=['POST'])
@token_required
def api_fulfill_request(current_user, request_id):
    # Only hospitals can fulfill blood requests
    if not isinstance(current_user, Hospital):
        return jsonify({'success': False, 'message': 'Only hospitals can fulfill blood requests'}), 403
    
    result = fulfill_blood_request(request_id, current_user.id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@blood_bank_api.route('/hospital/requests', methods=['GET'])
@token_required
def api_get_hospital_requests(current_user):
    # Only hospitals can view their requests
    if not isinstance(current_user, Hospital):
        return jsonify({'success': False, 'message': 'Only hospitals can view their requests'}), 403
    
    try:
        requests = db_session.query(BloodRequest).filter_by(hospital_id=current_user.id).all()
        
        requests_data = [{
            'id': req.id,
            'blood_type': req.blood_type.value,
            'quantity_ml': req.quantity_ml,
            'urgency_level': req.urgency_level,
            'request_date': req.request_date.isoformat(),
            'fulfilled_date': req.fulfilled_date.isoformat() if req.fulfilled_date else None,
            'status': req.status
        } for req in requests]
        
        return jsonify({'success': True, 'requests': requests_data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error retrieving requests: {str(e)}'}), 400

# Donor routes
@blood_bank_api.route('/donor/donate', methods=['POST'])
@token_required
def api_record_donation(current_user):
    # Only donors can donate blood
    if not isinstance(current_user, Donor):
        return jsonify({'success': False, 'message': 'Only donors can donate blood'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['hospital_id', 'quantity_ml']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    # Check if donor is eligible (last donation was more than 3 months ago)
    if current_user.last_donation_date:
        three_months_ago = datetime.datetime.utcnow() - datetime.timedelta(days=90)
        if current_user.last_donation_date > three_months_ago:
            days_to_wait = (current_user.last_donation_date + datetime.timedelta(days=90) - datetime.datetime.utcnow()).days
            return jsonify({
                'success': False, 
                'message': f'You must wait {days_to_wait} more days before donating again'
            }), 400
    
    result = record_blood_donation(
        donor_id=current_user.id,
        hospital_id=data['hospital_id'],
        blood_type=current_user.blood_type,
        quantity_ml=data['quantity_ml']
    )
    
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@blood_bank_api.route('/donor/history', methods=['GET'])
@token_required
def api_get_donation_history(current_user):
    # Only donors can view their donation history
    if not isinstance(current_user, Donor):
        return jsonify({'success': False, 'message': 'Only donors can view their donation history'}), 403
    
    try:
        donations = db_session.query(BloodDonation).filter_by(donor_id=current_user.id).all()
        
        # Get hospital names
        hospital_ids = [donation.hospital_id for donation in donations]
        hospitals = {h.id: h.name for h in db_session.query(Hospital).filter(Hospital.id.in_(hospital_ids)).all()}
        
        donations_data = [{
            'id': donation.id,
            'hospital_id': donation.hospital_id,
            'hospital_name': hospitals.get(donation.hospital_id, 'Unknown Hospital'),
            'blood_type': donation.blood_type.value,
            'quantity_ml': donation.quantity_ml,
            'donation_date': donation.donation_date.isoformat()
        } for donation in donations]
        
        return jsonify({'success': True, 'donations': donations_data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error retrieving donation history: {str(e)}'}), 400

# Public routes
@blood_bank_api.route('/hospitals', methods=['GET'])
def api_get_hospitals():
    """Get list of all registered hospitals"""
    try:
        hospitals = db_session.query(Hospital).all()
        
        hospitals_data = [{
            'id': hospital.id,
            'name': hospital.name,
            'address': hospital.address,
            'contact_number': hospital.contact_number
        } for hospital in hospitals]
        
        return jsonify({'success': True, 'hospitals': hospitals_data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error retrieving hospitals: {str(e)}'}), 400

@blood_bank_api.route('/blood-types', methods=['GET'])
def api_get_blood_types():
    """Get list of all blood types"""
    blood_types = [blood_type.value for blood_type in BloodType]
    return jsonify({'success': True, 'blood_types': blood_types}), 200
