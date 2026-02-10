import os
import re
from typing import Dict, Any, Tuple

class Preprocessor:
    """
    Simple preprocessor for judgement documents only
    Extracts key information and prepares for summarization
    """
    
    def __init__(self):
        self.name = "Preprocessor"
    
    def process(self, file_path: str) -> Dict[str, Any]:
        """
        Process a judgement document
        Returns structured information
        """
        print(f"[Preprocessor] Processing file: {file_path}")
        
        try:
            # Step 1: Extract text from file
            text = self.extract_text_from_file(file_path)
            
            if not text:
                return {
                    "success": False,
                    "error": "Could not extract text from file"
                }
            
            # Step 2: Extract basic information
            info = self.extract_basic_info(text)
            
            # Step 3: Clean and structure the text
            structured_text = self.structure_judgement_text(text)
            
            return {
                "success": True,
                "file_path": file_path,
                "file_size": os.path.getsize(file_path),
                "original_text": text[:1000] + "..." if len(text) > 1000 else text,
                "extracted_info": info,
                "structured_text": structured_text,
                "word_count": len(text.split()),
                "paragraph_count": len(text.split('\n\n')),
                "preprocessed_for": "summarizer"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Preprocessing error: {str(e)}"
            }
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from various file formats"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.txt':
                return self.read_text_file(file_path)
            elif file_ext == '.pdf':
                return self.read_pdf_file(file_path)
            elif file_ext == '.docx':
                return self.read_docx_file(file_path)
            else:
                # Try to read as text file first
                try:
                    return self.read_text_file(file_path)
                except:
                    return f"[File type {file_ext} not fully supported. Please upload .txt, .pdf, or .docx]"
        
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    def read_text_file(self, file_path: str) -> str:
        """Read text file with UTF-8 encoding"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def read_pdf_file(self, file_path: str) -> str:
        """Read PDF file using PyPDF2"""
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            return "[PDF support requires PyPDF2. Please install: pip install PyPDF2]"
    
    def read_docx_file(self, file_path: str) -> str:
        """Read DOCX file using python-docx"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except ImportError:
            return "[DOCX support requires python-docx. Please install: pip install python-docx]"
    
    def extract_basic_info(self, text: str) -> Dict[str, Any]:
        """Extract basic information from judgement text"""
        info = {
            "case_number": self.extract_case_number(text),
            "court_name": self.extract_court_name(text),
            "parties": self.extract_parties(text),
            "judge_name": self.extract_judge_name(text),
            "date": self.extract_date(text),
            "sections_mentioned": self.extract_legal_sections(text),
        }
        return info
    
    def extract_case_number(self, text: str) -> str:
        """Extract case number from judgement text"""
        patterns = [
            r'Case No\.?\s*[:\.]?\s*([A-Za-z0-9\.\-\/]+)',
            r'CRL\.?\s*A\.?\s*([A-Za-z0-9\.\-\/]+)',
            r'CR\.?\s*P\.?\s*([A-Za-z0-9\.\-\/]+)',
            r'W\.?\s*P\.?\s*([A-Za-z0-9\.\-\/]+)',
            r'S\.?\s*L\.?\s*P\.?\s*([A-Za-z0-9\.\-\/]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Not found"
    
    def extract_court_name(self, text: str) -> str:
        """Extract court name from judgement text"""
        courts = [
            "Supreme Court of India",
            "High Court",
            "District Court",
            "Sessions Court",
            "Magistrate Court"
        ]
        
        for court in courts:
            if court.lower() in text.lower():
                return court
        
        # Check for "IN THE COURT OF" pattern
        match = re.search(r'IN THE (?:HIGH|SUPREME|DISTRICT|SESSION)\s+COURT', text, re.IGNORECASE)
        if match:
            return match.group(0)
        
        return "Court name not found"
    
    def extract_parties(self, text: str) -> list:
        """Extract parties involved (simplified)"""
        lines = text.split('\n')
        parties = []
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if 'appellant' in line_lower or 'petitioner' in line_lower or 'applicant' in line_lower:
                # Try to get the next line as party name
                if i + 1 < len(lines):
                    parties.append(f"Appellant/Petitioner: {lines[i+1].strip()}")
            elif 'respondent' in line_lower or 'state' in line_lower:
                if i + 1 < len(lines):
                    parties.append(f"Respondent/State: {lines[i+1].strip()}")
        
        # If not found, look for "vs" pattern
        if not parties:
            for line in text[:500].split('\n'):  # Check first 500 chars
                if ' v. ' in line or ' vs. ' in line or ' versus ' in line.lower():
                    parties = [part.strip() for part in re.split(r'v\.|vs\.|versus', line, flags=re.IGNORECASE)]
                    break
        
        return parties if parties else ["Parties not identified"]
    
    def extract_judge_name(self, text: str) -> str:
        """Extract judge's name"""
        lines = text.split('\n')
        
        for line in lines[:20]:  # Check first 20 lines
            line_lower = line.lower()
            if 'hon\'ble' in line_lower or 'justice' in line_lower or 'j.' in line_lower:
                # Clean the line
                name = re.sub(r'HON\'BLE|JUSTICE|J\.|MR\.|MRS\.|MS\.', '', line, flags=re.IGNORECASE)
                name = name.strip()
                if name and len(name.split()) <= 4:  # Reasonable name length
                    return name
        
        return "Judge name not found"
    
    def extract_date(self, text: str) -> str:
        """Extract date from judgement"""
        patterns = [
            r'Date\s*[:\.]\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'Dated\s*[:\.]\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "Date not found"
    
    def extract_legal_sections(self, text: str) -> list:
        """Extract mentioned legal sections"""
        patterns = [
            r'Section\s+(\d+[A-Z]*)\s+of\s+([A-Z\s]+Act|IPC|CrPC|CPC|Constitution)',
            r'under\s+Section\s+(\d+[A-Z]*)\s+of',
            r'S\.\s*(\d+[A-Z]*)\s+of',
        ]
        
        sections = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    section_text = f"Section {match[0]} of {match[1]}"
                else:
                    section_text = f"Section {match}"
                if section_text not in sections:
                    sections.append(section_text)
        
        return sections
    
    def structure_judgement_text(self, text: str) -> Dict[str, str]:
        """Structure judgement text into logical parts"""
        structure = {
            "header": "",
            "case_details": "",
            "facts": "",
            "issues": "",
            "arguments": "",
            "analysis": "",
            "decision": "",
            "order": "",
            "footer": ""
        }
        
        lines = text.split('\n')
        current_section = "header"
        section_buffer = []
        
        # Simple keyword-based section detection
        section_keywords = {
            "case_details": ["case no", "crl.a", "cr.p", "w.p", "s.l.p", "in the matter of"],
            "facts": ["facts", "brief facts", "factual matrix", "narration of facts"],
            "issues": ["issues", "question for consideration", "points for determination"],
            "arguments": ["arguments", "submissions", "contended that", "learned counsel"],
            "analysis": ["analysis", "consideration", "discussion", "scrutiny"],
            "decision": ["decision", "conclusion", "finding", "hold that"],
            "order": ["order", "operative portion", "in the result"]
        }
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line indicates a new section
            section_found = False
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Save current section
                    structure[current_section] = "\n".join(section_buffer)
                    # Start new section
                    current_section = section
                    section_buffer = [line]
                    section_found = True
                    break
            
            if not section_found:
                section_buffer.append(line)
        
        # Save the last section
        structure[current_section] = "\n".join(section_buffer)
        
        return structure