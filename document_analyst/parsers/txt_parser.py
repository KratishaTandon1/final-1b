"""
TXT Parser Module
Handles parsing of plain text documents.
"""

from typing import Dict, Any
import os

class TXTParser:
    """Parser for plain text documents."""
    
    def __init__(self):
        """Initialize the TXT parser."""
        pass
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a TXT file and extract content.
        
        Args:
            file_path (str): Path to the TXT file
            
        Returns:
            dict: Parsed content with metadata
        """
        try:
            # Get file metadata
            file_stats = os.stat(file_path)
            metadata = {
                'title': os.path.basename(file_path),
                'author': '',
                'subject': '',
                'creator': '',
                'file_size': file_stats.st_size,
                'created': file_stats.st_ctime,
                'modified': file_stats.st_mtime
            }
            
            # Read file content with encoding detection
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            content = ""
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        content = file.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if not content:
                raise Exception("Could not decode file with any supported encoding")
            
            # Split content into lines for analysis
            lines = content.split('\n')
            processed_lines = []
            
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                if line_stripped:  # Only include non-empty lines
                    processed_lines.append({
                        'line_number': i + 1,
                        'content': line_stripped
                    })
            
            metadata['num_lines'] = len(lines)
            metadata['num_non_empty_lines'] = len(processed_lines)
            
            return {
                'content': content,
                'metadata': metadata,
                'lines': processed_lines,
                'file_type': 'txt'
            }
            
        except Exception as e:
            raise Exception(f"Error parsing TXT file {file_path}: {str(e)}")
    
    def is_supported(self, file_path: str) -> bool:
        """Check if the file is a supported text file."""
        return file_path.lower().endswith(('.txt', '.text', '.md', '.markdown'))
