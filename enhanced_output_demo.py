"""
Demonstration of Enhanced Output Format
Shows the comprehensive metadata and section analysis structure.
"""

from document_analyst import DocumentAnalyst
from document_analyst.persona_templates import PersonaTemplates
from document_analyst.job_templates import JobTemplates
import json
import tempfile
import os

def create_sample_documents_for_enhanced_demo():
    """Create sample documents for enhanced output demonstration."""
    
    documents = []
    
    # Document 1: Research Paper
    research_content = """
Machine Learning in Healthcare: Clinical Applications and Challenges

Abstract
This paper presents a comprehensive review of machine learning applications in healthcare, focusing on clinical decision support systems, diagnostic imaging, and patient outcome prediction. We analyze 200+ studies published between 2020-2024.

Introduction
Healthcare organizations are increasingly adopting machine learning technologies to improve patient care, reduce costs, and enhance operational efficiency. This systematic review examines current applications and identifies key implementation challenges.

Methodology
We conducted a systematic literature search using PubMed, IEEE Digital Library, and Google Scholar. Inclusion criteria included peer-reviewed articles, clinical validation studies, and implementation case studies.

Key Findings
1. Diagnostic Imaging: 85% accuracy improvement in radiology
2. Clinical Decision Support: 30% reduction in diagnostic errors  
3. Drug Discovery: 40% faster compound identification
4. Patient Monitoring: Real-time risk assessment capabilities

Implementation Challenges
- Data privacy and security concerns
- Integration with existing EHR systems
- Regulatory compliance requirements
- Staff training and adoption barriers

Conclusion
Machine learning shows significant promise in healthcare applications. Success depends on addressing technical, regulatory, and organizational challenges through systematic implementation approaches.
    """
    
    # Document 2: Financial Report
    financial_content = """
TechHealth Corp - Q4 2024 Financial Report

Executive Summary
TechHealth Corp delivered exceptional financial performance in Q4 2024, with revenue growth of 28% year-over-year and improved profit margins across all business segments.

Financial Highlights
- Total Revenue: $2.4 billion (28% increase)
- Net Income: $480 million (35% increase) 
- Operating Margin: 22% (improved from 18%)
- Cash Flow: $650 million positive

Business Segment Performance
Healthcare Technology: $1.2B revenue, 32% growth
- AI diagnostics platform: 45% market share gain
- Clinical software solutions: $400M revenue
- Medical device integration: 25% growth

Financial Services Technology: $800M revenue, 22% growth
- Payment processing: $300M revenue
- Risk management software: 18% growth
- Compliance solutions: $200M revenue

Research & Development: $240M investment, 10% of revenue
- 15 new patents filed
- 3 major product launches
- Partnership with 5 leading hospitals

Market Position
TechHealth maintains leadership position in healthcare AI with 35% market share. Strong competitive moats include proprietary algorithms, extensive clinical partnerships, and regulatory expertise.

Risk Factors
- Regulatory changes in healthcare AI
- Increased competition from tech giants
- Data privacy legislation impact
- Economic uncertainty effects

Forward Guidance
Management expects 20-25% revenue growth in 2025, driven by expanded AI platform adoption and new market penetration.
    """
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f1:
        f1.write(research_content)
        doc1_path = f1.name
        documents.append(doc1_path)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f2:
        f2.write(financial_content)
        doc2_path = f2.name
        documents.append(doc2_path)
    
    return documents

def demonstrate_enhanced_output():
    """Demonstrate the enhanced output format with comprehensive metadata."""
    
    print("🎯 ENHANCED OUTPUT FORMAT DEMONSTRATION")
    print("=" * 80)
    print("Comprehensive Metadata and Section Analysis")
    print("=" * 80)
    
    # Create sample documents
    document_paths = create_sample_documents_for_enhanced_demo()
    
    # Initialize the analyst
    analyst = DocumentAnalyst()
    
    # Define test scenarios
    scenarios = [
        {
            'name': 'Healthcare Research Analysis',
            'persona': {
                'role': 'Healthcare Data Scientist',
                'experience_level': 'Senior',
                'domain': 'Healthcare Technology',
                'goals': ['clinical applications', 'machine learning', 'healthcare analytics', 'patient outcomes'],
                'keywords': ['healthcare', 'clinical', 'patient', 'medical', 'diagnosis', 'treatment', 'ai', 'machine learning'],
                'context_preferences': ['methodology', 'findings', 'clinical validation', 'implementation']
            },
            'job': 'Analyze machine learning applications in healthcare for clinical decision support system development'
        },
        {
            'name': 'Financial Investment Analysis',
            'persona': {
                'role': 'Investment Analyst',
                'experience_level': 'Senior',
                'domain': 'Financial Analysis',
                'goals': ['investment decisions', 'financial performance', 'market analysis', 'risk assessment'],
                'keywords': ['revenue', 'profit', 'growth', 'market', 'financial', 'investment', 'performance'],
                'context_preferences': ['financial highlights', 'market position', 'risk factors', 'guidance']
            },
            'job': 'Evaluate TechHealth Corp investment potential based on Q4 2024 financial performance and market position'
        }
    ]
    
    # Run analysis for each scenario
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🔍 SCENARIO {i}: {scenario['name']}")
        print("=" * 60)
        
        # Run analysis with enhanced output
        results = analyst.analyze_documents(
            document_paths=document_paths,
            persona=scenario['persona'],
            job_to_be_done=scenario['job'],
            top_k=3,
            enhanced_output=True
        )
        
        # Display key sections of the enhanced output
        print(f"\n📋 METADATA SECTION:")
        print("-" * 30)
        metadata = results['metadata']
        print(f"Analysis ID: {results['analysis_id']}")
        print(f"Processing Timestamp: {metadata['processing_timestamp']}")
        print(f"Total Documents: {metadata['analysis_settings']['total_documents_processed']}")
        print(f"Total Sections: {metadata['analysis_settings']['total_sections_analyzed']}")
        
        print(f"\nPersona: {metadata['persona']['role']} ({metadata['persona']['experience_level']})")
        print(f"Domain: {metadata['persona']['domain']}")
        print(f"Job Type: {metadata['job_to_be_done']['task_type']}")
        print(f"Complexity: {metadata['job_to_be_done']['complexity_level']}")
        
        print(f"\nInput Documents:")
        for doc in metadata['input_documents']:
            print(f"  - {doc['filename']} ({doc['file_type']}) [ID: {doc['document_id']}]")
        
        print(f"\n📄 EXTRACTED SECTIONS:")
        print("-" * 30)
        for section in results['extracted_sections'][:2]:  # Show top 2
            print(f"\nSection {section['section_id']} (Rank: {section['importance_rank']})")
            print(f"Document: {section['document']['filename']}")
            print(f"Page: {section['page_number']}")
            print(f"Title: {section['section_title']}")
            print(f"Relevance Score: {section['relevance_score']}")
            print(f"Word Count: {section['word_count']}")
            print(f"Confidence: {section['extraction_metadata']['confidence_level']}")
            
            print(f"Score Breakdown:")
            breakdown = section['score_breakdown']
            print(f"  - Total: {breakdown['total_score']}")
            print(f"  - TF-IDF: {breakdown['tfidf_score']}")
            print(f"  - Keyword: {breakdown['keyword_score']}")
            print(f"  - Semantic: {breakdown['semantic_score']}")
            
            print(f"Content Preview: {section['content_preview']}")
        
        print(f"\n🔍 SUB-SECTION ANALYSIS:")
        print("-" * 30)
        for subsection in results['subsection_analysis'][:2]:  # Show top 2
            print(f"\nSubsection {subsection['subsection_id']}")
            print(f"Parent: {subsection['parent_section_id']}")
            print(f"Document: {subsection['document']['filename']} ({subsection['document']['source_type']})")
            print(f"Page Range: {subsection['page_number_constraints']['page_range']}")
            
            print(f"Content Analysis:")
            analysis = subsection['content_analysis']
            print(f"  - Domain Relevance: {analysis['domain_relevance']}")
            print(f"  - Job Alignment: {analysis['job_alignment']}")
            print(f"  - Information Density: {analysis['information_density']}")
            
            print(f"Quality Metrics:")
            quality = subsection['quality_metrics']
            print(f"  - Readability: {quality['readability_score']}")
            print(f"  - Completeness: {quality['completeness']}")
            print(f"  - Specificity: {quality['specificity']}")
            
            print(f"Key Concepts: {', '.join(subsection['content_analysis']['key_concepts'][:5])}")
            
            print(f"Refined Text: {subsection['refined_text'][:200]}...")
        
        print(f"\n📊 SUMMARY STATISTICS:")
        print("-" * 30)
        stats = results['summary_statistics']
        print(f"Total Sections Found: {stats['total_sections_found']}")
        print(f"Average Relevance Score: {stats['average_relevance_score']:.3f}")
        print(f"Highest Scoring Document: {stats['highest_scoring_document']}")
        print(f"Processing Time: {stats['processing_time_ms']} ms")
        
        print(f"Content Distribution:")
        for doc, count in stats['content_distribution'].items():
            print(f"  - {doc}: {count} sections")
        
        print(f"\n💡 RECOMMENDATIONS:")
        print("-" * 30)
        for rec in results['recommendations']:
            print(f"• {rec}")
        
        # Save detailed results to file
        output_filename = f"enhanced_analysis_scenario_{i}.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Detailed results saved to: {output_filename}")
    
    # Cleanup temporary files
    print(f"\n🧹 CLEANUP:")
    for doc_path in document_paths:
        try:
            os.unlink(doc_path)
            print(f"Deleted: {os.path.basename(doc_path)}")
        except:
            pass
    
    print(f"\n" + "=" * 80)
    print("🎉 ENHANCED OUTPUT FORMAT DEMONSTRATION COMPLETE!")
    print("The system now provides comprehensive metadata including:")
    print("✅ 1. Metadata: Input docs, persona, job, processing timestamp")
    print("✅ 2. Extracted Sections: Document, page, title, importance rank")
    print("✅ 3. Sub-section Analysis: Refined text, page constraints, quality metrics")
    print("✅ Plus: Content analysis, quality scoring, and recommendations")
    print("=" * 80)

if __name__ == "__main__":
    demonstrate_enhanced_output()
