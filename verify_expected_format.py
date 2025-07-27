"""
Output Format Verification Script
Validates that all challenge outputs match the expected format exactly.
"""

import json
import os
from typing import Dict, Any

def verify_expected_format(output_file: str) -> Dict[str, Any]:
    """Verify that output file matches expected format."""
    
    print(f"\n🔍 Verifying: {output_file}")
    
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check required top-level keys
    required_keys = ['metadata', 'extracted_sections', 'subsection_analysis']
    missing_keys = [key for key in required_keys if key not in data]
    
    if missing_keys:
        print(f"❌ Missing required keys: {missing_keys}")
        return {'status': 'FAILED', 'errors': [f"Missing keys: {missing_keys}"]}
    
    errors = []
    
    # Verify metadata structure
    metadata = data['metadata']
    metadata_checks = {
        'input_documents': list,
        'persona': str,
        'job_to_be_done': str,
        'processing_timestamp': str
    }
    
    for field, expected_type in metadata_checks.items():
        if field not in metadata:
            errors.append(f"Missing metadata.{field}")
        elif not isinstance(metadata[field], expected_type):
            errors.append(f"metadata.{field} should be {expected_type.__name__}, got {type(metadata[field]).__name__}")
    
    # Verify extracted_sections structure
    sections = data['extracted_sections']
    if not isinstance(sections, list) or len(sections) != 5:
        errors.append(f"extracted_sections should be list of 5 items, got {len(sections) if isinstance(sections, list) else type(sections).__name__}")
    else:
        for i, section in enumerate(sections):
            required_section_fields = ['document', 'section_title', 'importance_rank', 'page_number']
            for field in required_section_fields:
                if field not in section:
                    errors.append(f"extracted_sections[{i}] missing {field}")
    
    # Verify subsection_analysis structure
    subsections = data['subsection_analysis']
    if not isinstance(subsections, list) or len(subsections) != 5:
        errors.append(f"subsection_analysis should be list of 5 items, got {len(subsections) if isinstance(subsections, list) else type(subsections).__name__}")
    else:
        for i, subsection in enumerate(subsections):
            required_subsection_fields = ['document', 'refined_text', 'page_number']
            for field in required_subsection_fields:
                if field not in subsection:
                    errors.append(f"subsection_analysis[{i}] missing {field}")
    
    # Check for unexpected fields (should only have the 3 required keys)
    unexpected_keys = [key for key in data.keys() if key not in required_keys]
    if unexpected_keys:
        errors.append(f"Unexpected top-level keys: {unexpected_keys}")
    
    if errors:
        print(f"❌ Format issues found:")
        for error in errors:
            print(f"   • {error}")
        return {'status': 'FAILED', 'errors': errors}
    else:
        print(f"✅ Perfect format match!")
        return {
            'status': 'PASSED',
            'documents': len(metadata['input_documents']),
            'persona': metadata['persona'],
            'sections': len(sections),
            'subsections': len(subsections)
        }

def main():
    """Verify all collection outputs."""
    
    print("🎯 OUTPUT FORMAT VERIFICATION")
    print("=" * 50)
    
    collections = [
        "Collection 1/challenge1b_output.json",
        "Collection 2/challenge1b_output.json", 
        "Collection 3/challenge1b_output.json"
    ]
    
    results = {}
    all_passed = True
    
    for collection in collections:
        if os.path.exists(collection):
            result = verify_expected_format(collection)
            results[collection] = result
            if result['status'] == 'FAILED':
                all_passed = False
        else:
            print(f"\n❌ File not found: {collection}")
            all_passed = False
    
    print(f"\n📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    for collection, result in results.items():
        collection_name = collection.split('/')[0]
        status = "✅ PASSED" if result['status'] == 'PASSED' else "❌ FAILED"
        print(f"{collection_name}: {status}")
        
        if result['status'] == 'PASSED':
            print(f"   📄 Documents: {result['documents']}")
            print(f"   👤 Persona: {result['persona']}")
            print(f"   📝 Sections: {result['sections']}")
            print(f"   🔍 Subsections: {result['subsections']}")
    
    print(f"\n🎉 OVERALL RESULT: {'✅ ALL COLLECTIONS MATCH EXPECTED FORMAT' if all_passed else '❌ SOME COLLECTIONS HAVE FORMAT ISSUES'}")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
