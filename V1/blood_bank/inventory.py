from .models import BloodInventory, BloodRequest, BloodDonation, BloodType, Notification, init_db
import datetime

# Initialize database session
db_session = init_db()

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

def fulfill_blood_request(request_id, hospital_id):
    """Fulfill a blood request from hospital inventory"""
    try:
        blood_request = db_session.query(BloodRequest).filter_by(id=request_id).first()
        if not blood_request:
            return {'success': False, 'message': 'Blood request not found'}
            
        if blood_request.status != "Pending":
            return {'success': False, 'message': f'Request is already {blood_request.status}'}
            
        # Check if hospital has enough blood
        inventory = db_session.query(BloodInventory).filter_by(
            hospital_id=hospital_id,
            blood_type=blood_request.blood_type,
            is_available=True
        ).all()
        
        available_quantity = sum(item.quantity_ml for item in inventory 
                               if item.expiry_date > datetime.datetime.utcnow())
        
        if available_quantity < blood_request.quantity_ml:
            return {'success': False, 'message': 'Not enough blood in inventory'}
            
        # Use blood from inventory (oldest first)
        remaining_quantity = blood_request.quantity_ml
        for item in sorted(inventory, key=lambda x: x.expiry_date):
            if item.expiry_date <= datetime.datetime.utcnow():
                continue
                
            if item.quantity_ml <= remaining_quantity:
                remaining_quantity -= item.quantity_ml
                item.is_available = False
            else:
                item.quantity_ml -= remaining_quantity
                remaining_quantity = 0
                
            if remaining_quantity == 0:
                break
                
        # Update request status
        blood_request.status = "Fulfilled"
        blood_request.fulfilled_date = datetime.datetime.utcnow()
        
        db_session.commit()
        return {'success': True, 'message': 'Blood request fulfilled successfully'}
    except Exception as e:
        db_session.rollback()
        return {'success': False, 'message': f'Error fulfilling request: {str(e)}'}

def record_blood_donation(donor_id, hospital_id, blood_type, quantity_ml):
    """Record a blood donation from a donor"""
    try:
        # Record the donation
        new_donation = BloodDonation(
            donor_id=donor_id,
            hospital_id=hospital_id,
            blood_type=blood_type,
            quantity_ml=quantity_ml,
            donation_date=datetime.datetime.utcnow()
        )
        db_session.add(new_donation)
        
        # Add to hospital inventory
        expiry_date = datetime.datetime.utcnow() + datetime.timedelta(days=42)  # Blood expires in 42 days
        new_inventory = BloodInventory(
            hospital_id=hospital_id,
            blood_type=blood_type,
            quantity_ml=quantity_ml,
            expiry_date=expiry_date,
            is_available=True
        )
        db_session.add(new_inventory)
        
        # Update donor's last donation date
        donor = db_session.query(Donor).filter_by(id=donor_id).first()
        if donor:
            donor.last_donation_date = datetime.datetime.utcnow()
            
        db_session.commit()
        return {'success': True, 'message': 'Blood donation recorded successfully'}
    except Exception as e:
        db_session.rollback()
        return {'success': False, 'message': f'Error recording donation: {str(e)}'}

def notify_eligible_donors(blood_type):
    """Create notifications for eligible donors of a specific blood type"""
    try:
        # Find eligible donors who haven't donated in the last 3 months
        three_months_ago = datetime.datetime.utcnow() - datetime.timedelta(days=90)
        eligible_donors = db_session.query(Donor).filter_by(
            blood_type=blood_type,
            is_eligible=True
        ).filter(
            (Donor.last_donation_date == None) | (Donor.last_donation_date <= three_months_ago)
        ).all()
        
        for donor in eligible_donors:
            notification = Notification(
                recipient_email=donor.email,
                subject="Urgent Blood Donation Request",
                message=f"Dear {donor.name}, there is an urgent need for your blood type ({blood_type.value}). "
                        f"Please consider donating blood at your earliest convenience.",
                is_sent=False
            )
            db_session.add(notification)
            
        db_session.commit()
        return {'success': True, 'message': f'Notifications created for {len(eligible_donors)} eligible donors'}
    except Exception as e:
        db_session.rollback()
        return {'success': False, 'message': f'Error creating notifications: {str(e)}'}
