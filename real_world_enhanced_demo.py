"""
Real-World Enhanced Output Demonstration
Using actual document collections with comprehensive output format.
"""

import os
import json
from document_analyst import DocumentAnalyst
from document_analyst.persona_templates import PersonaTemplates
from document_analyst.job_templates import JobTemplates

def demonstrate_real_collections_enhanced_output():
    """Demonstrate enhanced output using real document collections."""
    
    print("🎯 REAL-WORLD ENHANCED OUTPUT DEMONSTRATION")
    print("=" * 80)
    print("Using Actual Document Collections with Comprehensive Output")
    print("=" * 80)
    
    # Initialize the analyst
    analyst = DocumentAnalyst()
    
    # Define real-world scenarios using existing collections
    scenarios = [
        {
            'name': 'Travel Planning Analysis',
            'collection_path': 'Collection 1',
            'documents': [
                'Collection 1/PDFs/South of France - Cities.pdf',
                'Collection 1/PDFs/South of France - Cuisine.pdf',
                'Collection 1/PDFs/South of France - History.pdf',
                'Collection 1/PDFs/South of France - Restaurants and Hotels.pdf',
                'Collection 1/PDFs/South of France - Things to Do.pdf'
            ],
            'persona': {
                'role': 'Travel Planner',
                'experience_level': 'Senior',
                'domain': 'Tourism & Travel',
                'goals': ['itinerary planning', 'cultural experiences', 'accommodation', 'dining recommendations'],
                'keywords': ['travel', 'tourism', 'restaurants', 'hotels', 'attractions', 'culture', 'activities'],
                'context_preferences': ['recommendations', 'practical information', 'local insights', 'tips']
            },
            'job': 'Plan a comprehensive 4-day cultural and culinary tour of South of France for a group of 10 college friends'
        },
        {
            'name': 'PDF Management Training',
            'collection_path': 'Collection 2',
            'documents': [
                'Collection 2/PDFs/Learn Acrobat - Create and Convert_1.pdf',
                'Collection 2/PDFs/Learn Acrobat - Edit_1.pdf',
                'Collection 2/PDFs/Learn Acrobat - Fill and Sign.pdf',
                'Collection 2/PDFs/Learn Acrobat - Share_1.pdf',
                'Collection 2/PDFs/The Ultimate PDF Sharing Checklist.pdf'
            ],
            'persona': {
                'role': 'HR Training Specialist',
                'experience_level': 'Senior',
                'domain': 'Human Resources & Training',
                'goals': ['employee training', 'document management', 'workflow optimization', 'compliance'],
                'keywords': ['training', 'documents', 'forms', 'workflow', 'management', 'efficiency', 'compliance'],
                'context_preferences': ['step-by-step guides', 'best practices', 'workflows', 'checklists']
            },
            'job': 'Develop comprehensive PDF management training program for HR staff to handle employee onboarding documents and forms'
        },
        {
            'name': 'Menu Development Strategy',
            'collection_path': 'Collection 3',
            'documents': [
                'Collection 3/PDFs/Breakfast Ideas.pdf',
                'Collection 3/PDFs/Dinner Ideas - Mains_1.pdf',
                'Collection 3/PDFs/Dinner Ideas - Sides_1.pdf',
                'Collection 3/PDFs/Lunch Ideas.pdf'
            ],
            'persona': {
                'role': 'Corporate Food Service Manager',
                'experience_level': 'Senior',
                'domain': 'Food Service Management',
                'goals': ['menu planning', 'dietary requirements', 'cost optimization', 'nutrition balance'],
                'keywords': ['food', 'menu', 'nutrition', 'dietary', 'vegetarian', 'gluten-free', 'catering'],
                'context_preferences': ['recipes', 'nutritional information', 'dietary options', 'serving suggestions']
            },
            'job': 'Create balanced vegetarian buffet menu with gluten-free options for corporate wellness program'
        }
    ]
    
    # Process each scenario
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🔍 SCENARIO {i}: {scenario['name']}")
        print("=" * 60)
        
        # Check if documents exist
        existing_docs = []
        for doc in scenario['documents']:
            if os.path.exists(doc):
                existing_docs.append(doc)
            else:
                print(f"⚠️  Document not found: {doc}")
        
        if not existing_docs:
            print(f"❌ No documents found for {scenario['name']}")
            continue
        
        print(f"📁 Processing {len(existing_docs)} documents from {scenario['collection_path']}")
        
        try:
            # Run analysis with enhanced output
            results = analyst.analyze_documents(
                document_paths=existing_docs,
                persona=scenario['persona'],
                job_to_be_done=scenario['job'],
                top_k=5,
                enhanced_output=True
            )
            
            # Display structured output
            print(f"\n📋 1. METADATA SECTION")
            print("-" * 40)
            metadata = results['metadata']
            
            print(f"Analysis ID: {results['analysis_id']}")
            print(f"Processing Timestamp: {metadata['processing_timestamp']}")
            
            print(f"\na. Input Documents ({len(metadata['input_documents'])} total):")
            for doc in metadata['input_documents']:
                print(f"   • {doc['filename']} [{doc['file_type'].upper()}] (ID: {doc['document_id']})")
            
            print(f"\nb. Persona Configuration:")
            persona = metadata['persona']
            print(f"   • Role: {persona['role']}")
            print(f"   • Experience: {persona['experience_level']}")
            print(f"   • Domain: {persona['domain']}")
            print(f"   • Goals: {', '.join(persona['goals'][:3])}...")
            
            print(f"\nc. Job-to-be-Done:")
            job_info = metadata['job_to_be_done']
            print(f"   • Task: {job_info['task_description']}")
            print(f"   • Type: {job_info['task_type']}")
            print(f"   • Complexity: {job_info['complexity_level']}")
            
            print(f"\nd. Processing Info:")
            settings = metadata['analysis_settings']
            print(f"   • Documents Processed: {settings['total_documents_processed']}")
            print(f"   • Sections Analyzed: {settings['total_sections_analyzed']}")
            print(f"   • Scoring Method: {settings['scoring_method']}")
            
            print(f"\n📄 2. EXTRACTED SECTIONS")
            print("-" * 40)
            
            for j, section in enumerate(results['extracted_sections'][:3], 1):
                print(f"\nSection {j}:")
                print(f"a. Document: {section['document']['filename']}")
                print(f"b. Page Number: {section['page_number']}")
                print(f"c. Section Title: {section['section_title']}")
                print(f"d. Importance Rank: {section['importance_rank']}")
                print(f"   • Relevance Score: {section['relevance_score']}")
                print(f"   • Word Count: {section['word_count']}")
                print(f"   • Confidence: {section['extraction_metadata']['confidence_level']}")
                
                # Score breakdown
                breakdown = section['score_breakdown']
                print(f"   • Score Breakdown: TF-IDF({breakdown['tfidf_score']}), Keyword({breakdown['keyword_score']}), Semantic({breakdown['semantic_score']})")
            
            print(f"\n🔍 3. SUB-SECTION ANALYSIS")
            print("-" * 40)
            
            for j, subsection in enumerate(results['subsection_analysis'][:3], 1):
                print(f"\nSub-section {j}:")
                print(f"a. Document: {subsection['document']['filename']} ({subsection['document']['source_type']})")
                print(f"b. Parent Section: {subsection['parent_section_id']}")
                print(f"c. Refined Text: {subsection['refined_text'][:150]}...")
                print(f"d. Page Number Constraints:")
                constraints = subsection['page_number_constraints']
                print(f"   • Start Page: {constraints['start_page']}")
                print(f"   • End Page: {constraints['end_page']}")
                print(f"   • Page Range: {constraints['page_range']}")
                print(f"   • Total Pages: {constraints['total_pages_covered']}")
                
                # Content analysis
                analysis = subsection['content_analysis']
                print(f"   • Domain Relevance: {analysis['domain_relevance']}")
                print(f"   • Job Alignment: {analysis['job_alignment']}")
                print(f"   • Information Density: {analysis['information_density']}")
                
                # Quality metrics
                quality = subsection['quality_metrics']
                print(f"   • Quality: Readability({quality['readability_score']}), Completeness({quality['completeness']}), Specificity({quality['specificity']})")
                
                # Key concepts
                concepts = subsection['content_analysis']['key_concepts'][:5]
                print(f"   • Key Concepts: {', '.join(concepts)}")
            
            print(f"\n📊 SUMMARY & RECOMMENDATIONS")
            print("-" * 40)
            stats = results['summary_statistics']
            print(f"Total Sections: {stats['total_sections_found']}")
            print(f"Average Score: {stats['average_relevance_score']:.3f}")
            print(f"Top Document: {stats['highest_scoring_document']}")
            print(f"Processing Time: {stats['processing_time_ms']} ms")
            
            print(f"\nContent Distribution:")
            for doc, count in stats['content_distribution'].items():
                print(f"  • {doc}: {count} sections")
            
            print(f"\nRecommendations:")
            for rec in results['recommendations']:
                print(f"  • {rec}")
            
            # Save results
            output_filename = f"enhanced_real_analysis_{scenario['name'].lower().replace(' ', '_')}.json"
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Complete analysis saved to: {output_filename}")
            
        except Exception as e:
            print(f"❌ Error processing {scenario['name']}: {str(e)}")
            continue
    
    print(f"\n" + "=" * 80)
    print("🎉 REAL-WORLD ENHANCED OUTPUT DEMONSTRATION COMPLETE!")
    print("")
    print("✅ COMPREHENSIVE OUTPUT STRUCTURE DEMONSTRATED:")
    print("1. Metadata Section:")
    print("   a. Input documents (filename, type, ID)")
    print("   b. Persona (role, experience, domain, goals)")
    print("   c. Job-to-be-done (task, type, complexity)")
    print("   d. Processing timestamp and settings")
    print("")
    print("2. Extracted Sections:")
    print("   a. Document identification")
    print("   b. Page number location")
    print("   c. Section title")
    print("   d. Importance rank with scoring details")
    print("")
    print("3. Sub-section Analysis:")
    print("   a. Document source information")
    print("   b. Parent section linkage")
    print("   c. Refined text content")
    print("   d. Page number constraints (start, end, range)")
    print("   + Content analysis and quality metrics")
    print("")
    print("🚀 SYSTEM READY FOR PRODUCTION DEPLOYMENT!")
    print("=" * 80)

if __name__ == "__main__":
    demonstrate_real_collections_enhanced_output()
