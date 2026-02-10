import os
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.helpers import get_groq_api_key

class Summarizer:
    """
    Summarizer Agent using LangChain + LLaMA-3 via Groq
    Summarizes legal documents in simple language without compromising accuracy
    """
    
    def __init__(self):
        self.name = "Summarizer"
        self.api_key = get_groq_api_key()
        self.llm = self._initialize_llm()
        self.templates = self._create_prompt_templates()
    
    def _initialize_llm(self):
        """Initialize the LLaMA-3 model via Groq"""
        try:
            # Using Llama3-8b-8192 which is fast and good for summarization
            llm = ChatGroq(
                groq_api_key=self.api_key,
                model_name="llama-3.1-8b-instant",
                temperature=0.3,  # Lower temperature for more factual outputs
                max_tokens=2048,
            )
            print(f"[Summarizer] Initialized with model: llama3-8b-8192")
            return llm
        except Exception as e:
            print(f"[Summarizer] Error initializing LLM: {e}")
            raise
    
    def _create_prompt_templates(self) -> Dict[str, Any]:
        """Create prompt templates for different document types"""
        
        # Base system prompt for legal summarization
        system_prompt = """You are a legal document summarization expert. Your task is to summarize legal documents 
        in simple, understandable language for common people while maintaining absolute accuracy of legal facts.
        
        Guidelines:
        1. Keep summaries concise but comprehensive
        2. Use simple language without legal jargon
        3. Highlight key points: parties, issues, decisions, orders
        4. Mention relevant laws/sections but explain them simply
        5. Maintain original meaning and legal correctness
        6. Structure the summary logically
        7. Avoid personal opinions or interpretations"""
        
        # Template for judgement summaries
        judgement_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", """DOCUMENT TYPE: Judgement

Please summarize the following judgement document:

Document Information:
- Case Number: {case_number}
- Court: {court}
- Judge: {judge}
- Date: {date}

Document Content:
{document_text}

Provide a summary with these sections:
1. **Case Overview**: Brief description of what the case is about
2. **Key Parties**: Who is involved (appellant, respondent, etc.)
3. **Main Issues**: What legal questions were being decided
4. **Court's Decision**: What the court decided
5. **Key Legal Points**: Important laws/sections cited
6. **Final Order**: What happens next (sentences, orders, etc.)
7. **Simple Explanation**: One paragraph explaining the case in simplest terms

Keep each section concise. Use bullet points where helpful.""")
        ])
        
        # Template for bail application summaries
        bail_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", """DOCUMENT TYPE: Bail Application

Please summarize the following bail application:

Document Information:
- Application Number: {case_number}
- Court: {court}

Document Content:
{document_text}

Provide a summary with these sections:
1. **Applicant Details**: Who is applying for bail
2. **Charges**: What offenses are they charged with
3. **Grounds for Bail**: Why they believe they should get bail
4. **Legal Basis**: Which laws/sections they're citing
5. **Court's Decision** (if mentioned): Whether bail was granted
6. **Conditions** (if any): Any conditions imposed by court
7. **Simple Explanation**: One paragraph in simplest terms

Use simple language that a non-lawyer can understand.""")
        ])
        
        # Template for generic legal documents
        generic_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", """DOCUMENT TYPE: Legal Document

Please summarize the following legal document:

Document Content:
{document_text}

Provide a comprehensive summary covering:
1. **Document Purpose**: What this document is for
2. **Key Parties**: Who is involved
3. **Main Content**: What the document says
4. **Legal References**: Any laws/sections mentioned
5. **Important Points**: Critical information to know
6. **Simple Summary**: One paragraph in plain language""")
        ])
        
        return {
            "system_prompt": system_prompt,
            "judgement": judgement_template,
            "bail": bail_template,
            "generic": generic_template
        }
    
    def summarize(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize a legal document
        
        Args:
            document_data: Dictionary containing document information
                Required keys: 'document_type', 'text', 'extracted_info'
                
        Returns:
            Dictionary containing the summary
        """
        print(f"[Summarizer] Summarizing {document_data.get('document_type', 'unknown')} document")
        
        try:
            # Extract data
            doc_type = document_data.get('document_type', 'generic')
            text = document_data.get('text', '')
            extracted_info = document_data.get('extracted_info', {})
            
            if not text:
                return {
                    "success": False,
                    "error": "No document text provided for summarization"
                }
            
            # Truncate text if too long (LLaMA has token limits)
            max_length = 6000  # characters
            if len(text) > max_length:
                print(f"[Summarizer] Truncating document from {len(text)} to {max_length} characters")
                text = text[:max_length] + "... [document truncated for length]"
            
            # Get appropriate template
            template = self.templates.get(doc_type, self.templates["generic"])
            
            # Prepare variables for template
            template_vars = {
                "document_text": text,
                "case_number": extracted_info.get('case_number', 'Not specified'),
                "court": extracted_info.get('court_name', 'Not specified'),
                "judge": extracted_info.get('judge_name', 'Not specified'),
                "date": extracted_info.get('date', 'Not specified'),
            }
            
            # Create chain
            chain = template | self.llm | StrOutputParser()
            
            # Call the LLM
            print(f"[Summarizer] Calling LLaMA-3 via Groq API...")
            summary_text = chain.invoke(template_vars)
            
            # Extract structured information if possible
            structured_summary = self._extract_structured_summary(summary_text, doc_type)
            
            return {
                "success": True,
                "document_type": doc_type,
                "original_length": len(text),
                "summary": summary_text,
                "structured_summary": structured_summary,
                "summary_length": len(summary_text),
                "compression_ratio": f"{len(summary_text)/len(text)*100:.1f}%" if text else "N/A",
                "model_used": "llama3-8b-8192",
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            print(f"[Summarizer] Error during summarization: {e}")
            return {
                "success": False,
                "error": f"Summarization failed: {str(e)}",
                "document_type": document_data.get('document_type', 'unknown')
            }
    
    def _extract_structured_summary(self, summary_text: str, doc_type: str) -> Dict[str, Any]:
        """Extract structured information from the summary"""
        structured = {
            "key_points": [],
            "legal_sections": [],
            "parties": [],
            "decision": "",
            "simple_explanation": ""
        }
        
        try:
            # Simple parsing of the summary text
            lines = summary_text.split('\n')
            
            # Look for key sections
            current_section = None
            for line in lines:
                line_lower = line.lower()
                
                # Extract simple explanation
                if 'simple explanation' in line_lower or 'simplest terms' in line_lower:
                    current_section = "simple_explanation"
                    continue
                elif 'decision' in line_lower and 'court' in line_lower:
                    current_section = "decision"
                    continue
                elif 'legal points' in line_lower or 'laws' in line_lower:
                    current_section = "legal_sections"
                    continue
                elif 'parties' in line_lower:
                    current_section = "parties"
                    continue
                
                # Add content to current section
                if current_section and line.strip() and not line.strip().startswith('**'):
                    if current_section == "simple_explanation":
                        structured["simple_explanation"] += line.strip() + " "
                    elif current_section == "decision":
                        structured["decision"] += line.strip() + " "
                    elif current_section in ["parties", "legal_sections"]:
                        if line.strip().startswith('-') or line.strip().startswith('•'):
                            structured[current_section].append(line.strip()[1:].strip())
            
            # Clean up
            for key in ["simple_explanation", "decision"]:
                if key in structured:
                    structured[key] = structured[key].strip()
            
            # Extract legal sections using regex
            import re
            legal_patterns = [
                r'Section\s+(\d+[A-Z]*)',
                r'under\s+Section\s+(\d+[A-Z]*)',
                r'IPC\s+Section\s+(\d+)',
                r'CrPC\s+Section\s+(\d+)'
            ]
            
            for pattern in legal_patterns:
                matches = re.findall(pattern, summary_text, re.IGNORECASE)
                for match in matches:
                    if match not in structured["legal_sections"]:
                        structured["legal_sections"].append(match)
            
            return structured
            
        except Exception as e:
            print(f"[Summarizer] Error extracting structured summary: {e}")
            return structured
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def summarize_simple(self, text: str, doc_type: str = "generic") -> str:
        """
        Simple summarization interface
        
        Args:
            text: Document text to summarize
            doc_type: Type of document
            
        Returns:
            Summary text
        """
        document_data = {
            "document_type": doc_type,
            "text": text,
            "extracted_info": {}
        }
        
        result = self.summarize(document_data)
        
        if result["success"]:
            return result["summary"]
        else:
            return f"Error: {result.get('error', 'Unknown error')}"