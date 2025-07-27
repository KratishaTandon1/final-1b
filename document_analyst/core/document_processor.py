"""
Document Processor Module
Handles parsing and processing of different document formats.
"""

import os
from typing import List, Dict, Any
from ..parsers.pdf_parser import PDFParser
from ..parsers.docx_parser import DOCXParser
from ..parsers.txt_parser import TXTParser
from ..utils.text_processing import TextProcessor

class DocumentProcessor:
    """Main document processing class."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the document processor.
        
        Args:
            config (dict): Configuration parameters
        """
        self.config = config or {}
        self.text_processor = TextProcessor(self.config)
        
        # Initialize parsers
        self.parsers = {
            '.pdf': PDFParser(),
            '.docx': DOCXParser(),
            '.doc': DOCXParser(),
            '.txt': TXTParser(),
        }
    
    def process_document(self, document_path: str) -> List[Dict[str, Any]]:
        """
        Process a document and extract sections.
        
        Args:
            document_path (str): Path to the document
            
        Returns:
            list: List of document sections with metadata
        """
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Document not found: {document_path}")
        
        # Get file extension
        _, ext = os.path.splitext(document_path.lower())
        
        if ext not in self.parsers:
            raise ValueError(f"Unsupported file format: {ext}")
        
        # Parse document content
        parser = self.parsers[ext]
        raw_content = parser.parse(document_path)
        
        # Process and segment content
        sections = self.text_processor.segment_content(raw_content)
        
        # Add metadata to each section
        for i, section in enumerate(sections):
            section.update({
                'document_path': document_path,
                'section_id': i,
                'file_type': ext,
                'processing_timestamp': self._get_timestamp()
            })
        
        return sections
    
    def process_multiple_documents(self, document_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple documents.
        
        Args:
            document_paths (list): List of document paths
            
        Returns:
            list: Combined list of all document sections
        """
        all_sections = []
        
        for doc_path in document_paths:
            try:
                sections = self.process_document(doc_path)
                all_sections.extend(sections)
            except Exception as e:
                print(f"Error processing {doc_path}: {str(e)}")
                continue
        
        return all_sections
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for metadata."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        return list(self.parsers.keys())
