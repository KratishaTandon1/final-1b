"""
Text Processing Utilities
Handles text segmentation, cleaning, and preprocessing.
"""

import re
from typing import List, Dict, Any
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

class TextProcessor:
    """Handles text processing and segmentation."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the text processor.
        
        Args:
            config (dict): Configuration parameters
        """
        self.config = config or {}
        self.min_section_length = self.config.get('min_section_length', 100)
        self.max_section_length = self.config.get('max_section_length', 2000)
        
        # Download required NLTK data if not present
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
    
    def segment_content(self, raw_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Segment document content into meaningful sections.
        
        Args:
            raw_content (dict): Raw content from document parser
            
        Returns:
            list: List of document sections
        """
        content_text = raw_content.get('content', '')
        file_type = raw_content.get('file_type', 'unknown')
        
        if not content_text.strip():
            return []
        
        sections = []
        
        if file_type == 'pdf':
            sections = self._segment_pdf_content(raw_content)
        elif file_type == 'docx':
            sections = self._segment_docx_content(raw_content)
        elif file_type == 'txt':
            sections = self._segment_txt_content(raw_content)
        else:
            # Generic segmentation
            sections = self._segment_generic_content(content_text)
        
        # Post-process sections
        processed_sections = []
        for section in sections:
            processed_section = self._process_section(section)
            if self._is_valid_section(processed_section):
                processed_sections.append(processed_section)
        
        return processed_sections
    
    def _segment_pdf_content(self, raw_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Segment PDF content."""
        sections = []
        pages = raw_content.get('pages', [])
        
        for page in pages:
            page_content = page.get('content', '').strip()
            if page_content:
                # Try to identify sections within the page
                page_sections = self._identify_sections_by_structure(page_content)
                
                for i, section_content in enumerate(page_sections):
                    sections.append({
                        'content': section_content,
                        'title': f"Page {page['page_number']} - Section {i+1}",
                        'source': f"page_{page['page_number']}",
                        'section_type': 'page_section'
                    })
        
        return sections
    
    def _segment_docx_content(self, raw_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Segment DOCX content."""
        sections = []
        paragraphs = raw_content.get('paragraphs', [])
        
        current_section = ""
        current_title = ""
        section_count = 1
        
        for para in paragraphs:
            para_content = para.get('content', '').strip()
            para_style = para.get('style', 'Normal')
            
            # Check if this paragraph is a heading
            if self._is_heading_style(para_style) or self._looks_like_heading(para_content):
                # Save previous section if it exists
                if current_section.strip():
                    sections.append({
                        'content': current_section.strip(),
                        'title': current_title or f"Section {section_count}",
                        'source': 'document',
                        'section_type': 'heading_section'
                    })
                    section_count += 1
                
                # Start new section
                current_title = para_content
                current_section = ""
            else:
                current_section += para_content + "\n"
        
        # Add final section
        if current_section.strip():
            sections.append({
                'content': current_section.strip(),
                'title': current_title or f"Section {section_count}",
                'source': 'document',
                'section_type': 'heading_section'
            })
        
        return sections
    
    def _segment_txt_content(self, raw_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Segment plain text content."""
        content = raw_content.get('content', '')
        
        # Try to identify sections by common patterns
        sections = self._identify_sections_by_structure(content)
        
        result_sections = []
        for i, section_content in enumerate(sections):
            result_sections.append({
                'content': section_content,
                'title': f"Section {i+1}",
                'source': 'text_file',
                'section_type': 'text_section'
            })
        
        return result_sections
    
    def _segment_generic_content(self, content: str) -> List[Dict[str, Any]]:
        """Generic content segmentation."""
        sections = self._identify_sections_by_structure(content)
        
        result_sections = []
        for i, section_content in enumerate(sections):
            result_sections.append({
                'content': section_content,
                'title': f"Section {i+1}",
                'source': 'generic',
                'section_type': 'generic_section'
            })
        
        return result_sections
    
    def _identify_sections_by_structure(self, content: str) -> List[str]:
        """Identify sections based on text structure."""
        # Split by double newlines first
        paragraphs = re.split(r'\n\s*\n', content)
        
        sections = []
        current_section = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Check if this looks like a section break
            if self._looks_like_section_break(para):
                if current_section:
                    sections.append(current_section)
                    current_section = para + "\n"
            else:
                current_section += para + "\n\n"
            
            # If section is getting too long, break it
            if len(current_section) > self.max_section_length:
                sections.append(current_section)
                current_section = ""
        
        # Add final section
        if current_section:
            sections.append(current_section)
        
        # If we only have one very long section, split it by sentences
        if len(sections) == 1 and len(sections[0]) > self.max_section_length:
            sections = self._split_by_sentences(sections[0])
        
        return sections
    
    def _split_by_sentences(self, text: str) -> List[str]:
        """Split long text into smaller sections by sentences."""
        sentences = sent_tokenize(text)
        sections = []
        current_section = ""
        
        for sentence in sentences:
            if len(current_section + sentence) > self.max_section_length:
                if current_section:
                    sections.append(current_section.strip())
                    current_section = sentence + " "
                else:
                    # Single sentence is too long, add it anyway
                    sections.append(sentence)
            else:
                current_section += sentence + " "
        
        if current_section:
            sections.append(current_section.strip())
        
        return sections
    
    def _is_heading_style(self, style: str) -> bool:
        """Check if a style indicates a heading."""
        heading_styles = ['Heading', 'Title', 'Subtitle']
        return any(heading in style for heading in heading_styles)
    
    def _looks_like_heading(self, text: str) -> bool:
        """Check if text looks like a heading."""
        if len(text) > 100:  # Headings are usually short
            return False
        
        # Check for heading patterns
        heading_patterns = [
            r'^\d+\.?\s+[A-Z]',  # "1. Introduction" or "1 Introduction"
            r'^[A-Z][A-Z\s]+$',  # "INTRODUCTION"
            r'^[A-Z][a-z\s]+:$',  # "Introduction:"
        ]
        
        for pattern in heading_patterns:
            if re.match(pattern, text.strip()):
                return True
        
        return False
    
    def _looks_like_section_break(self, text: str) -> bool:
        """Check if text looks like a section break."""
        return (self._looks_like_heading(text) or 
                len(text) < 50 and text.isupper() or
                re.match(r'^#+\s+', text))  # Markdown headings
    
    def _process_section(self, section: Dict[str, Any]) -> Dict[str, Any]:
        """Process and clean a section."""
        content = section.get('content', '')
        
        # Clean the content
        cleaned_content = self._clean_text(content)
        
        # Extract keywords
        keywords = self._extract_keywords(cleaned_content)
        
        # Add processed fields
        section.update({
            'content': cleaned_content,
            'word_count': len(cleaned_content.split()),
            'keywords': keywords,
            'char_count': len(cleaned_content)
        })
        
        return section
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', ' ', text)
        
        # Remove extra spaces
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Tokenize and filter
        words = word_tokenize(text.lower())
        
        # Filter out stop words and short words
        keywords = [word for word in words 
                   if word not in self.stop_words 
                   and len(word) > 2 
                   and word.isalpha()]
        
        # Get unique keywords
        return list(set(keywords))
    
    def _is_valid_section(self, section: Dict[str, Any]) -> bool:
        """Check if a section is valid for analysis."""
        content = section.get('content', '')
        word_count = section.get('word_count', 0)
        
        # Filter out sections that are too short or empty
        return (word_count >= self.min_section_length / 10 and  # Roughly 10 words minimum
                len(content.strip()) > 0)
