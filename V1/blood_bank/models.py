from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum
import datetime

Base = declarative_base()

class BloodType(enum.Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class Hospital(Base):
    __tablename__ = 'hospitals'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    contact_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    blood_requests = relationship("BloodRequest", back_populates="hospital")
    blood_donations = relationship("BloodDonation", back_populates="hospital")
    
class Donor(Base):
    __tablename__ = 'donors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    blood_type = Column(Enum(BloodType), nullable=False)
    address = Column(String(200), nullable=False)
    contact_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    last_donation_date = Column(DateTime, nullable=True)
    is_eligible = Column(Boolean, default=True)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    donations = relationship("BloodDonation", back_populates="donor")
    
class BloodInventory(Base):
    __tablename__ = 'blood_inventory'
    
    id = Column(Integer, primary_key=True)
    blood_type = Column(Enum(BloodType), nullable=False)
    quantity_ml = Column(Float, nullable=False, default=0)
    expiry_date = Column(DateTime, nullable=False)
    is_available = Column(Boolean, default=True)
    hospital_id = Column(Integer, ForeignKey('hospitals.id'), nullable=False)
    
class BloodRequest(Base):
    __tablename__ = 'blood_requests'
    
    id = Column(Integer, primary_key=True)
    hospital_id = Column(Integer, ForeignKey('hospitals.id'), nullable=False)
    blood_type = Column(Enum(BloodType), nullable=False)
    quantity_ml = Column(Float, nullable=False)
    urgency_level = Column(Integer, nullable=False)  # 1-5, 5 being most urgent
    request_date = Column(DateTime, default=datetime.datetime.utcnow)
    fulfilled_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="Pending")  # Pending, Fulfilled, Cancelled
    
    # Relationships
    hospital = relationship("Hospital", back_populates="blood_requests")
    
class BloodDonation(Base):
    __tablename__ = 'blood_donations'
    
    id = Column(Integer, primary_key=True)
    donor_id = Column(Integer, ForeignKey('donors.id'), nullable=False)
    hospital_id = Column(Integer, ForeignKey('hospitals.id'), nullable=False)
    blood_type = Column(Enum(BloodType), nullable=False)
    quantity_ml = Column(Float, nullable=False)
    donation_date = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    donor = relationship("Donor", back_populates="donations")
    hospital = relationship("Hospital", back_populates="blood_donations")
    
class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    recipient_email = Column(String(100), nullable=False)
    subject = Column(String(100), nullable=False)
    message = Column(String(500), nullable=False)
    is_sent = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    sent_date = Column(DateTime, nullable=True)

# Database initialization function
def init_db(db_path='sqlite:///blood_bank.db'):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
