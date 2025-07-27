"""
PDF Parser Module
Handles parsing of PDF documents.
"""

import PyPDF2
from typing import Dict, Any

class PDFParser:
    """Parser for PDF documents."""
    
    def __init__(self):
        """Initialize the PDF parser."""
        pass
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a PDF file and extract content.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            dict: Parsed content with metadata
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract metadata
                metadata = {
                    'title': '',
                    'author': '',
                    'subject': '',
                    'creator': '',
                    'num_pages': len(pdf_reader.pages)
                }
                
                if pdf_reader.metadata:
                    metadata.update({
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'creator': pdf_reader.metadata.get('/Creator', '')
                    })
                
                # Extract text content
                full_text = ""
                page_contents = []
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        full_text += page_text + "\n"
                        page_contents.append({
                            'page_number': page_num + 1,
                            'content': page_text
                        })
                    except Exception as e:
                        print(f"Error extracting text from page {page_num + 1}: {str(e)}")
                        continue
                
                return {
                    'content': full_text,
                    'metadata': metadata,
                    'pages': page_contents,
                    'file_type': 'pdf'
                }
                
        except Exception as e:
            raise Exception(f"Error parsing PDF file {file_path}: {str(e)}")
    
    def is_supported(self, file_path: str) -> bool:
        """Check if the file is a supported PDF."""
        return file_path.lower().endswith('.pdf')
