"""
Example usage of the Document Analyst system.
"""

from document_analyst import DocumentAnalyst
import json

def basic_example():
    """Basic usage example."""
    
    # Initialize the analyst
    analyst = DocumentAnalyst()
    
    # Define persona
    persona = {
        "role": "Data Scientist",
        "experience_level": "Senior",
        "domain": "Healthcare",
        "goals": ["machine learning", "data analysis", "statistical modeling"]
    }
    
    # Define job-to-be-done
    job_to_be_done = "Find best practices for implementing machine learning models in healthcare data analysis"
    
    # Example document paths (replace with actual paths)
    document_paths = [
        "sample_documents/ml_healthcare.pdf",
        "sample_documents/data_science_guide.docx",
        "sample_documents/clinical_analytics.txt"
    ]
    
    try:
        # Analyze documents
        results = analyst.analyze_documents(
            document_paths=document_paths,
            persona=persona,
            job_to_be_done=job_to_be_done,
            top_k=5
        )
        
        # Display results
        print("Analysis Results:")
        print("=" * 50)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Document: {result['document']}")
            print(f"   Section: {result.get('title', 'Untitled')}")
            print(f"   Relevance Score: {result['score']:.3f}")
            print(f"   Word Count: {result.get('word_count', 'N/A')}")
            print(f"   Content Preview: {result['content'][:200]}...")
            
            if 'score_breakdown' in result:
                breakdown = result['score_breakdown']
                print(f"   Score Breakdown:")
                print(f"     - TF-IDF: {breakdown.get('tfidf', 0):.3f}")
                print(f"     - Keyword: {breakdown.get('keyword', 0):.3f}")
                print(f"     - Semantic: {breakdown.get('semantic', 0):.3f}")
    
    except FileNotFoundError as e:
        print(f"Document not found: {e}")
        print("Please ensure the document paths exist or use the demo mode.")
    except Exception as e:
        print(f"Error during analysis: {e}")

def persona_examples():
    """Examples of different persona configurations."""
    
    personas = {
        "data_scientist": {
            "role": "Data Scientist",
            "experience_level": "Senior",
            "domain": "Healthcare",
            "goals": ["machine learning", "predictive modeling", "statistical analysis"]
        },
        
        "software_engineer": {
            "role": "Software Engineer",
            "experience_level": "Senior",
            "domain": "Technology",
            "goals": ["system architecture", "scalability", "performance optimization"]
        },
        
        "product_manager": {
            "role": "Product Manager",
            "experience_level": "Lead",
            "domain": "SaaS",
            "goals": ["user experience", "market research", "feature prioritization"]
        },
        
        "researcher": {
            "role": "Research Scientist",
            "experience_level": "Senior",
            "domain": "AI/ML",
            "goals": ["deep learning", "neural networks", "research methodology"]
        }
    }
    
    job_examples = {
        "data_scientist": "Identify best practices for building reliable ML pipelines in production",
        "software_engineer": "Find architectural patterns for building scalable microservices",
        "product_manager": "Discover user research methodologies for B2B products",
        "researcher": "Understand latest developments in transformer architectures"
    }
    
    print("Persona Examples:")
    print("=" * 50)
    
    for role, persona in personas.items():
        print(f"\n{role.replace('_', ' ').title()}:")
        print(f"  Persona: {json.dumps(persona, indent=4)}")
        print(f"  Example Job: {job_examples[role]}")

def configuration_example():
    """Example of using custom configuration."""
    
    # Custom configuration
    custom_config = {
        'min_section_length': 50,
        'max_section_length': 1500,
        'tfidf_weight': 0.5,
        'keyword_weight': 0.3,
        'semantic_weight': 0.2
    }
    
    # Initialize with custom config
    analyst = DocumentAnalyst(config=custom_config)
    
    print("Custom Configuration Example:")
    print("=" * 50)
    print(f"Configuration: {json.dumps(custom_config, indent=2)}")

if __name__ == "__main__":
    print("Document Analyst Examples")
    print("=" * 60)
    
    print("\n1. Basic Example:")
    basic_example()
    
    print("\n\n2. Persona Examples:")
    persona_examples()
    
    print("\n\n3. Configuration Example:")
    configuration_example()
