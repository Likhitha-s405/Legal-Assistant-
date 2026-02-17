import re
import PyPDF2
import docx
from geopy.geocoders import Nominatim
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CaseParser:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="legal_assistant")
        
        # Case type keywords
        self.case_types = {
            'divorce': ['divorce', 'marriage dissolution', 'separation', 'alimony'],
            'child_custody': ['child custody', 'visitation rights', 'parental rights'],
            'personal_injury': ['personal injury', 'accident', 'negligence', 'injury'],
            'criminal_defense': ['criminal', 'theft', 'assault', 'dui', 'felony'],
            'bankruptcy': ['bankruptcy', 'debt relief', 'insolvency'],
            'contract_dispute': ['contract', 'breach', 'agreement', 'dispute'],
            'property_law': ['property', 'real estate', 'landlord', 'tenant'],
            'employment_law': ['employment', 'labor', 'workplace', 'discrimination'],
            'immigration': ['immigration', 'visa', 'green card', 'citizenship'],
            'family_law': ['family law', 'adoption', 'guardianship']
        }
    
    def read_file(self, file_path: str) -> str:
        
        """Read text from file"""
        text = ""
        try:
            if file_path.endswith('.pdf'):
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
            
            elif file_path.endswith('.docx'):
                doc = docx.Document(file_path)
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
            
            elif file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
            
            logger.info(f"Successfully read file: {file_path}")
        except Exception as e:
            logger.error(f"Error reading file: {e}")
        
        return text
    
    def extract_case_type(self, text: str) -> str:
        """Extract case type from text"""
        text_lower = text.lower()
        
        for case_type, keywords in self.case_types.items():
            for keyword in keywords:
                if keyword in text_lower:
                    logger.info(f"Detected case type: {case_type}")
                    return case_type
        
        return "general"
    
    def extract_location(self, text: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
        """Extract location from text"""
        # Look for patterns like "City, ST" or "City, State"
        patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*([A-Z]{2})\b',  # City, ST
            r'\b(in|at|near)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*([A-Z]{2})\b',  # in City, ST
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                # Extract the city and state from the match
                groups = match.groups()
                if len(groups) == 2:
                    location_str = f"{groups[0]}, {groups[1]}"
                else:
                    location_str = f"{groups[1]}, {groups[2]}"
                
                try:
                    location = self.geolocator.geocode(location_str)
                    if location:
                        logger.info(f"Found location: {location_str}")
                        return (location.latitude, location.longitude, location_str)
                except Exception as e:
                    logger.warning(f"Geocoding failed for {location_str}: {e}")
        
        return (None, None, None)
    
    def parse_case_file(self, file_path: str) -> dict:
        """Parse case file and extract information"""
        text = self.read_file(file_path)
        
        if not text:
            return {
                'case_type': 'unknown',
                'location': {'latitude': None, 'longitude': None, 'name': None},
                'full_text': ''
            }
        
        case_type = self.extract_case_type(text)
        lat, lng, location_name = self.extract_location(text)
        
        return {
            'case_type': case_type,
            'location': {
                'latitude': lat,
                'longitude': lng,
                'name': location_name
            },
            'full_text': text[:1000]  # Store preview
        }