"""
Configuration module for the Document Analyst system.
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for Document Analyst."""
    
    def __init__(self):
        """Initialize configuration with default values."""
        self.config = {
            # Text processing settings
            'min_section_length': int(os.getenv('MIN_SECTION_LENGTH', 100)),
            'max_section_length': int(os.getenv('MAX_SECTION_LENGTH', 2000)),
            
            # Scoring weights
            'tfidf_weight': float(os.getenv('TFIDF_WEIGHT', 0.4)),
            'keyword_weight': float(os.getenv('KEYWORD_WEIGHT', 0.4)),
            'semantic_weight': float(os.getenv('SEMANTIC_WEIGHT', 0.2)),
            
            # Processing settings
            'max_documents': int(os.getenv('MAX_DOCUMENTS', 100)),
            'enable_caching': os.getenv('ENABLE_CACHING', 'true').lower() == 'true',
            
            # Output settings
            'default_top_k': int(os.getenv('DEFAULT_TOP_K', 10)),
            'include_score_breakdown': os.getenv('INCLUDE_SCORE_BREAKDOWN', 'true').lower() == 'true',
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values."""
        self.config.update(updates)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self.config.copy()

# Global configuration instance
config = Config()
