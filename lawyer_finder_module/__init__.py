# __init__.py - Fixed indentation
from case_parser import CaseParser
from lawyer_finder import LawyerFinder
from models import Lawyer, Base

class LegalCaseAnalyzer:
    def __init__(self, db_path=None):
        """Initialize the lawyer finder module"""
        self.case_parser = CaseParser()
        self.lawyer_finder = LawyerFinder(db_path) if db_path else LawyerFinder()
    
    # NEW METHOD - Add this with proper indentation (4 spaces inside the class)
    def find_lawyers_near_me(self, case_type: str = "general", max_distance: int = 25):
        """
        Find lawyers near your current location (auto-detected)
        
        Args:
            case_type: Type of legal case (e.g., 'divorce', 'personal_injury')
            max_distance: Search radius in kilometers
        
        Returns:
            dict: Results with lawyers near your location
        """
        print(f"\n🔍 Finding lawyers near you for {case_type} cases...")
        
        # Use the lawyer_finder's IP location method
        result = self.lawyer_finder.find_lawyers_near_ip(case_type, max_distance)
        
        if result.get('success', False) is False and result.get('status') == 'location_not_found':
            print("⚠️  Could not auto-detect your location.")
            return result
        
        return result
    
    # EXISTING METHOD 1
    def analyze_case_file(self, file_path, max_distance=25):
        """Analyze a case file and find matching lawyers"""
        case_info = self.case_parser.parse_case_file(file_path)
        
        if not case_info['full_text']:
            return {
                'success': False,
                'error': 'Could not read file',
                'case_info': case_info
            }
        
        results = self.lawyer_finder.find_lawyers_by_case(
            case_info, 
            max_distance=max_distance
        )
        
        return {
            'success': True,
            'case_info': {
                'case_type': case_info['case_type'],
                'location': case_info['location']['name'],
                'coordinates': {
                    'lat': case_info['location']['latitude'],
                    'lng': case_info['location']['longitude']
                }
            },
            'results': results
        }
    
    # EXISTING METHOD 2
    def add_lawyer(self, lawyer_data):
        """Add a new lawyer to the database"""
        return self.lawyer_finder.add_lawyer(lawyer_data)
    
    # EXISTING METHOD 3
    def get_lawyer_by_id(self, lawyer_id):
        """Get lawyer details by ID"""
        return self.lawyer_finder.get_lawyer(lawyer_id)
    
    # EXISTING METHOD 4
    def search_lawyers(self, specialization=None, city=None, state=None):
        """Search lawyers by criteria"""
        return self.lawyer_finder.search_lawyers(
            specialization=specialization,
            city=city,
            state=state
        )

# Export the classes
__all__ = ['LegalCaseAnalyzer', 'Lawyer', 'CaseParser', 'LawyerFinder', 'Base']