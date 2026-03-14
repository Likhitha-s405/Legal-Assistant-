from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Lawyer(Base):
    __tablename__ = 'lawyers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    firm_name = Column(String(200))
    specialization = Column(String(100))
    experience_years = Column(Integer)
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(String(200))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'firm_name': self.firm_name,
            'specialization': self.specialization,
            'experience_years': self.experience_years,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'location': {
                'lat': self.latitude,
                'lng': self.longitude
            }
        }

class CaseAnalysis(Base):
    """Store case analysis history (optional)"""
    __tablename__ = 'case_analyses'
    
    id = Column(Integer, primary_key=True)
    file_name = Column(String(200))
    case_type = Column(String(50))
    location_found = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    lawyers_found = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)