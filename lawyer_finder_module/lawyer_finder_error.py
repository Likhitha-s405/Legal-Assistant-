from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geopy.distance import geodesic
from models import Lawyer, Base
import os
import logging

logger = logging.getLogger(__name__)

class LawyerFinder:
    def __init__(self, db_path=None):
        """Initialize with optional database path"""
        if db_path:
            self.engine = create_engine(f'sqlite:///{db_path}')
        else:
            # Default to local database
            db_dir = os.path.dirname(os.path.abspath(__file__))
            self.engine = create_engine(f'sqlite:///{db_dir}/lawyers.db')
        
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
def find_lawyers_by_case(self, case_info: dict, max_distance: int = 25, limit: int = 10):
    """Find lawyers based on case info - FIXED DUPLICATION ISSUE"""
    
    case_type = case_info['case_type']
    client_lat = case_info['location']['latitude']
    client_lng = case_info['location']['longitude']
    
    # If no location found, return by specialization
    if not client_lat or not client_lng:
        return {
            'status': 'location_not_found',
            'case_type': case_type,
            'message': 'Location not found in case file',
            'recommendations': self.get_lawyers_by_specialization(case_type, limit)
        }
    
    client_location = (client_lat, client_lng)
    lawyers = self.session.query(Lawyer).all()
    
    # Use a dictionary to prevent duplicates (key by lawyer id)
    nearby_lawyers_dict = {}
    
    for lawyer in lawyers:
        if lawyer.latitude and lawyer.longitude:
            lawyer_location = (lawyer.latitude, lawyer.longitude)
            
            try:
                distance = geodesic(client_location, lawyer_location).kilometers
                
                if distance <= max_distance:
                    # Only add if not already in dictionary
                    if lawyer.id not in nearby_lawyers_dict:
                        lawyer_data = lawyer.to_dict()
                        lawyer_data['distance_km'] = round(distance, 2)
                        lawyer_data['exact_match'] = (
                            case_type.lower() in lawyer.specialization.lower() 
                            if lawyer.specialization else False
                        )
                        nearby_lawyers_dict[lawyer.id] = lawyer_data
            except Exception as e:
                logger.warning(f"Error calculating distance for lawyer {lawyer.id}: {e}")
                continue
    
    # Convert dictionary back to list
    nearby_lawyers = list(nearby_lawyers_dict.values())
    
    # Sort by exact match first, then by distance
    nearby_lawyers.sort(key=lambda x: (not x.get('exact_match', False), x['distance_km']))
    
             # Save analysis (optional)
        self._save_analysis(case_info, len(nearby_lawyers))
        
        return {
            'status': 'success',
            'case_type': case_type,
            'location': case_info['location']['name'],
            'coordinates': {'lat': client_lat, 'lng': client_lng},
            'max_distance_km': max_distance,
            'total_found': len(nearby_lawyers),
            'lawyers': nearby_lawyers[:limit]
        }
    
    def get_lawyers_by_specialization(self, specialization: str, limit: int = 10):
        """Get lawyers by specialization"""
        if specialization == 'general':
            lawyers = self.session.query(Lawyer).limit(limit).all()
        else:
            lawyers = self.session.query(Lawyer).filter(
                Lawyer.specialization.ilike(f'%{specialization}%')
            ).limit(limit).all()
        
        return [lawyer.to_dict() for lawyer in lawyers]
    
    def add_lawyer(self, lawyer_data):
        """Add a new lawyer to database"""
        try:
            lawyer = Lawyer(**lawyer_data)
            self.session.add(lawyer)
            self.session.commit()
            logger.info(f"Added lawyer: {lawyer_data.get('name')}")
            return {'success': True, 'id': lawyer.id}
        except Exception as e:
            logger.error(f"Error adding lawyer: {e}")
            self.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def get_lawyer(self, lawyer_id):
        """Get lawyer by ID"""
        lawyer = self.session.query(Lawyer).get(lawyer_id)
        return lawyer.to_dict() if lawyer else None
    
    def search_lawyers(self, specialization=None, city=None, state=None):
        """Search lawyers by criteria"""
        query = self.session.query(Lawyer)
        
        if specialization:
            query = query.filter(Lawyer.specialization.ilike(f'%{specialization}%'))
        if city:
            query = query.filter(Lawyer.city.ilike(f'%{city}%'))
        if state:
            query = query.filter(Lawyer.state == state.upper())
        
        lawyers = query.limit(50).all()
        return [lawyer.to_dict() for lawyer in lawyers]
    
    def _save_analysis(self, case_info, lawyers_found):
        """Save case analysis (optional)"""
        try:
            analysis = CaseAnalysis(
                case_type=case_info['case_type'],
                location_found=case_info['location']['name'],
                latitude=case_info['location']['latitude'],
                longitude=case_info['location']['longitude'],
                lawyers_found=lawyers_found
            )
            self.session.add(analysis)
            self.session.commit()
        except:
            pass  # Non-critical, don't fail if analysis save fails
    
    def add_sample_data(self):
        """Add sample lawyers for testing - PREVENTS DUPLICATES"""
        # Check if lawyers already exist
    existing_count = self.session.query(Lawyer).count()
    if existing_count > 0:
        logger.info(f"Database already has {existing_count} lawyers. Skipping sample data.")
        return
    
    sample_lawyers = [
        {
            'name': 'John Smith',
            'firm_name': 'Smith & Associates',
            'specialization': 'divorce, family law',
            'experience_years': 15,
            'phone': '212-555-0101',
            'email': 'john.smith@smithlaw.com',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001',
            'latitude': 40.7500,
            'longitude': -73.9967
        },
        {
            'name': 'Sarah Johnson',
            'firm_name': 'Johnson Legal',
            'specialization': 'personal injury, medical malpractice',
            'experience_years': 10,
            'phone': '212-555-0102',
            'email': 'sarah@johnsonlegal.com',
            'address': '456 Park Ave',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10022',
            'latitude': 40.7580,
            'longitude': -73.9685
        },
        {
            'name': 'Michael Chen',
            'firm_name': 'Chen Law Office',
            'specialization': 'criminal defense, dui',
            'experience_years': 8,
            'phone': '212-555-0103',
            'email': 'michael@chenlaw.com',
            'address': '789 Broadway',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10003',
            'latitude': 40.7311,
            'longitude': -73.9883
        },
        {
            'name': 'Emily Rodriguez',
            'firm_name': 'Rodriguez & Partners',
            'specialization': 'immigration, family law',
            'experience_years': 12,
            'phone': '212-555-0104',
            'email': 'emily@rodriguezlaw.com',
            'address': '321 Lexingon Ave',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10016',
            'latitude': 40.7444,
            'longitude': -73.9767
        },
        {
            'name': 'David Kim',
            'firm_name': 'Kim & Associates',
            'specialization': 'business law, contracts',
            'experience_years': 20,
            'phone': '212-555-0105',
            'email': 'david@kimlaw.com',
            'address': '555 5th Ave',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10017',
            'latitude': 40.7559,
            'longitude': -73.9786
        }
    ]
    
    for lawyer_data in sample_lawyers:
        # Check if lawyer already exists by email or name
        existing = self.session.query(Lawyer).filter_by(email=lawyer_data['email']).first()
        if not existing:
            lawyer = Lawyer(**lawyer_data)
            self.session.add(lawyer)
    
    self.session.commit()
    logger.info(f"Added {len(sample_lawyers)} sample lawyers")