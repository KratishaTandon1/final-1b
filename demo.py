"""
Simple example demonstrating the Document Analyst system.
"""

from document_analyst import DocumentAnalyst
import tempfile
import os

def create_sample_documents():
    """Create sample documents for demonstration."""
    
    documents = [
        {
            'filename': 'healthcare_ml.txt',
            'content': '''
Healthcare Machine Learning Implementation Guide

Introduction
This document provides comprehensive guidance for implementing machine learning solutions in healthcare environments. Healthcare data analysis requires special attention to privacy, accuracy, and regulatory compliance.

Data Preprocessing
Healthcare data often contains missing values, inconsistencies, and sensitive information. Key preprocessing steps include:
- Patient data anonymization and HIPAA compliance
- Handling missing clinical values appropriately  
- Feature engineering for clinical variables like vital signs and lab results
- Temporal data alignment for longitudinal patient records

Model Development
For diagnostic tasks, ensemble methods like Random Forest and Gradient Boosting show excellent performance. Deep learning approaches, particularly LSTM networks, excel at analyzing time-series patient data such as continuous monitoring data.

Validation and Testing
Healthcare ML models require rigorous validation strategies:
- Stratified cross-validation accounting for patient demographics
- Temporal validation for time-dependent predictions
- External validation on different hospital systems
- Clinical expert review of model predictions

Deployment Considerations
Production healthcare ML systems need:
- Real-time prediction capabilities
- Integration with Electronic Health Records (EHR)
- Continuous monitoring for model drift
- Audit trails for regulatory compliance
- Fail-safe mechanisms for critical decisions

Best Practices
- Always involve clinical domain experts in model development
- Implement robust data quality checks
- Ensure model interpretability for clinical decision support
- Regular retraining with new patient data
- Comprehensive documentation for regulatory review
            '''
        },
        {
            'filename': 'software_development.txt',
            'content': '''
Modern Software Development Practices

Overview
This guide covers essential practices for building robust, scalable software systems. Modern development emphasizes automation, collaboration, and continuous improvement.

Development Methodologies
Agile methodologies have become the standard for software development:
- Scrum framework for iterative development
- Kanban for continuous flow management
- DevOps practices for deployment automation
- Test-driven development (TDD) for quality assurance

Code Quality
Maintaining high code quality requires:
- Code review processes and pair programming
- Automated testing at unit, integration, and system levels
- Static code analysis and linting tools
- Consistent coding standards and style guides
- Refactoring practices to reduce technical debt

Architecture Patterns
Modern applications benefit from well-established patterns:
- Microservices for scalable, distributed systems
- Event-driven architecture for loose coupling
- Domain-driven design for complex business logic
- Clean architecture for maintainable codebases

Deployment and Operations
Reliable software delivery requires:
- Continuous integration and deployment (CI/CD)
- Infrastructure as code for consistent environments
- Containerization with Docker and Kubernetes
- Monitoring and logging for operational insights
- Automated rollback mechanisms for failed deployments

Security Considerations
Security must be built into every stage:
- Secure coding practices and vulnerability scanning
- Authentication and authorization frameworks
- Data encryption at rest and in transit
- Regular security audits and penetration testing
            '''
        }
    ]
    
    # Create temporary files
    temp_files = []
    for doc in documents:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(doc['content'])
            temp_files.append(f.name)
            print(f"Created sample document: {f.name}")
    
    return temp_files

def demonstrate_analysis():
    """Demonstrate the document analysis with different personas."""
    
    # Create sample documents
    print("Creating sample documents...")
    document_paths = create_sample_documents()
    
    try:
        # Initialize the analyzer
        analyst = DocumentAnalyst()
        
        # Define different personas and their jobs
        scenarios = [
            {
                'name': 'Healthcare Data Scientist',
                'persona': {
                    'role': 'Data Scientist',
                    'experience_level': 'Senior',
                    'domain': 'Healthcare',
                    'goals': ['machine learning', 'clinical data analysis', 'predictive modeling']
                },
                'job': 'Implement machine learning models for patient outcome prediction'
            },
            {
                'name': 'Software Architect',
                'persona': {
                    'role': 'Software Architect',
                    'experience_level': 'Lead',
                    'domain': 'Technology',
                    'goals': ['system design', 'scalability', 'microservices']
                },
                'job': 'Design scalable architecture for healthcare software systems'
            },
            {
                'name': 'Healthcare IT Manager',
                'persona': {
                    'role': 'IT Manager',
                    'experience_level': 'Senior',
                    'domain': 'Healthcare',
                    'goals': ['compliance', 'system integration', 'data security']
                },
                'job': 'Ensure HIPAA compliance and security in healthcare IT systems'
            }
        ]
        
        # Analyze documents for each scenario
        for scenario in scenarios:
            print(f"\n{'='*60}")
            print(f"SCENARIO: {scenario['name']}")
            print(f"{'='*60}")
            print(f"Persona: {scenario['persona']}")
            print(f"Job-to-be-done: {scenario['job']}")
            print("\nTop relevant sections:")
            print("-" * 40)
            
            # Perform analysis
            results = analyst.analyze_documents(
                document_paths=document_paths,
                persona=scenario['persona'],
                job_to_be_done=scenario['job'],
                top_k=3
            )
            
            # Display results
            for i, result in enumerate(results, 1):
                print(f"\n{i}. Document: {os.path.basename(result['document'])}")
                print(f"   Section: {result.get('title', 'Untitled')}")
                print(f"   Relevance Score: {result['score']:.3f}")
                print(f"   Content Preview: {result['content'][:300]}...")
                
                if 'score_breakdown' in result:
                    breakdown = result['score_breakdown']
                    print(f"   Score Details: TF-IDF={breakdown.get('tfidf', 0):.2f}, "
                          f"Keyword={breakdown.get('keyword', 0):.2f}, "
                          f"Semantic={breakdown.get('semantic', 0):.2f}")
    
    finally:
        # Clean up temporary files
        print(f"\nCleaning up temporary files...")
        for temp_file in document_paths:
            try:
                os.unlink(temp_file)
                print(f"Deleted: {temp_file}")
            except Exception as e:
                print(f"Error deleting {temp_file}: {e}")

if __name__ == "__main__":
    print("Document Analyst - Demonstration")
    print("=" * 50)
    
    demonstrate_analysis()
    
    print(f"\n{'='*60}")
    print("Demonstration completed!")
    print("=" * 60)
