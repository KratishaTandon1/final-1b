#!/usr/bin/env python3
"""Debug domain detection in the formatter."""

import json
from pathlib import Path
from expected_output_formatter import ExpectedOutputFormatter

def debug_collection_1():
    """Debug Collection 1 domain detection."""
    
    # Load Collection 1 input
    input_path = Path("Collection 1/challenge1b_input.json")
    with open(input_path) as f:
        challenge_data = json.load(f)
    
    print("Challenge Data:")
    print(f"Input documents: {challenge_data.get('input_documents', [])}")
    print(f"Description: {challenge_data.get('description', '')}")
    
    # Create formatter and test domain detection
    formatter = ExpectedOutputFormatter()
    formatter._current_challenge_data = challenge_data
    
    # Test domain detection with empty analysis sections
    analysis_sections = []
    domain = formatter._detect_domain(analysis_sections)
    print(f"Detected domain: {domain}")
    
    # Test with mock sections
    mock_sections = [
        {"document_path": "South of France - Cities.pdf"},
        {"document_path": "South of France - Things to Do.pdf"}
    ]
    domain2 = formatter._detect_domain(mock_sections)
    print(f"Domain with mock sections: {domain2}")

if __name__ == "__main__":
    debug_collection_1()
