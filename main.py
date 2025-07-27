"""Main CLI interface for the Document Analyst system."""
import json
import sys
import glob
from pathlib import Path
import click
from document_analyst import DocumentAnalyst
from document_analyst.persona_templates import PersonaTemplates
from document_analyst.job_templates import JobTemplates


@click.group()
def cli():
    """Intelligent Document Analyst - Extract and prioritize relevant document sections."""
    pass


@cli.command()
@click.option('--documents', '-d', required=True, help='Path to documents or glob pattern')
@click.option('--persona-file', '-p', help='Path to JSON file containing persona information')
@click.option('--persona-template', '-t', help='Use predefined persona template (researcher, student, financial_analyst, etc.)')
@click.option('--job', '-j', required=True, help='Job-to-be-done description')
@click.option('--output', '-o', help='Output file path (JSON format)')
@click.option('--top-k', '-k', default=10, help='Number of top results to return')
@click.option('--role', help='User role (if not using persona file/template)')
@click.option('--experience', help='Experience level (if not using persona file/template)')
@click.option('--domain', help='Domain/industry (if not using persona file/template)')
@click.option('--goals', help='Comma-separated goals (if not using persona file/template)')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed scoring breakdown')
def analyze(documents, persona_file, persona_template, job, output, top_k, role, experience, domain, goals, verbose):
    """Analyze documents and extract relevant sections."""
    
    try:
        # Load persona information
        if persona_file:
            with open(persona_file, 'r') as f:
                persona = json.load(f)
        elif persona_template:
            # Use predefined template
            template = PersonaTemplates.get_template(persona_template)
            if not template:
                available = PersonaTemplates.list_available_templates()
                click.echo(f"Error: Unknown persona template '{persona_template}'")
                click.echo(f"Available templates: {', '.join(available)}")
                sys.exit(1)
            persona = template.copy()
        else:
            # Build persona from command line arguments
            persona = {}
            if role:
                persona['role'] = role
            if experience:
                persona['experience_level'] = experience
            if domain:
                persona['domain'] = domain
            if goals:
                persona['goals'] = [g.strip() for g in goals.split(',')]
        
        if not persona:
            click.echo("Error: Must provide either --persona-file, --persona-template, or persona details via command line options")
            click.echo(f"Available persona templates: {', '.join(PersonaTemplates.list_available_templates())}")
            sys.exit(1)
        
        # Expand document paths
        if '*' in documents or '?' in documents:
            document_paths = glob.glob(documents)
        else:
            document_paths = [documents]
        
        if not document_paths:
            click.echo(f"Error: No documents found matching pattern: {documents}")
            sys.exit(1)
        
        # Initialize analyzer
        analyzer = DocumentAnalyst()
        
        # Analyze documents
        click.echo(f"Analyzing {len(document_paths)} documents...")
        results = analyzer.analyze_documents(
            document_paths=document_paths,
            persona=persona,
            job_to_be_done=job,
            top_k=top_k
        )
        
        # Output results
        if output:
            with open(output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            click.echo(f"Results saved to {output}")
        else:
            # Print to console
            click.echo(f"\nPersona: {persona.get('role', 'Unknown')} ({persona.get('domain', 'General')})")
            click.echo(f"Job: {job}")
            click.echo(f"\nTop {len(results)} relevant sections:\n")
            
            for i, result in enumerate(results, 1):
                click.echo(f"{i}. Document: {Path(result['document']).name}")
                click.echo(f"   Section: {result.get('title', 'Untitled')}")
                click.echo(f"   Relevance Score: {result['score']:.3f}")
                
                if verbose and 'score_breakdown' in result:
                    breakdown = result['score_breakdown']
                    click.echo(f"   Score Details: TF-IDF={breakdown.get('tfidf', 0):.3f}, "
                              f"Keyword={breakdown.get('keyword', 0):.3f}, "
                              f"Semantic={breakdown.get('semantic', 0):.3f}")
                
                click.echo(f"   Content Preview: {result['content'][:200]}...")
                if i < len(results):
                    click.echo("-" * 60)
    
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option('--role', prompt='Role', help='User role (e.g., Data Scientist, Software Engineer)')
@click.option('--experience', prompt='Experience level', help='Experience level (Junior, Senior, Lead)')
@click.option('--domain', prompt='Domain', help='Domain/industry (e.g., Healthcare, Finance)')
@click.option('--goals', prompt='Goals (comma-separated)', help='User goals and interests')
@click.option('--output', '-o', default='persona.json', help='Output file for persona')
def create_persona(role, experience, domain, goals, output):
    """Create a persona configuration file."""
    
    persona = {
        'role': role,
        'experience_level': experience,
        'domain': domain,
        'goals': [g.strip() for g in goals.split(',')]
    }
    
    with open(output, 'w') as f:
        json.dump(persona, f, indent=2)
    
    click.echo(f"Persona saved to {output}")


@cli.command()
def list_personas():
    """List all available persona templates."""
    
    click.echo("Available Persona Templates:")
    click.echo("=" * 40)
    
    templates = PersonaTemplates.list_available_templates()
    for template_name in templates:
        template = PersonaTemplates.get_template(template_name)
        click.echo(f"\n{template_name}:")
        click.echo(f"  Role: {template['role']}")
        click.echo(f"  Domain: {template['domain']}")
        click.echo(f"  Experience: {template['experience_level']}")
        click.echo(f"  Goals: {', '.join(template['goals'][:3])}...")


@cli.command()
@click.argument('persona_type')
def suggest_jobs(persona_type):
    """Suggest job-to-be-done templates for a persona type."""
    
    template = PersonaTemplates.get_template(persona_type)
    if not template:
        available = PersonaTemplates.list_available_templates()
        click.echo(f"Error: Unknown persona template '{persona_type}'")
        click.echo(f"Available templates: {', '.join(available)}")
        sys.exit(1)
    
    jobs = JobTemplates.suggest_job_for_persona(template['role'], template['domain'])
    
    click.echo(f"Suggested Jobs for {template['role']}:")
    click.echo("=" * 50)
    
    for job_name, job_details in jobs.items():
        click.echo(f"\n{job_name.replace('_', ' ').title()}:")
        click.echo(f"  Description: {job_details['description']}")
        click.echo(f"  Focus Areas: {', '.join(job_details['focus_areas'])}")


@cli.command()
def demo():
    """Run a demonstration with sample data."""
    
    # Create sample documents
    sample_docs = [
        {
            'name': 'ml_best_practices.txt',
            'content': '''Machine Learning Best Practices in Healthcare

Introduction
Machine learning has revolutionized healthcare data analysis, enabling predictive modeling for patient outcomes, disease diagnosis, and treatment optimization. This document outlines key best practices for implementing ML models in healthcare settings.

Data Quality and Preprocessing
High-quality data is crucial for successful ML implementations. Healthcare data often contains missing values, inconsistencies, and privacy concerns. Key preprocessing steps include:
- Data cleaning and validation
- Handling missing values appropriately
- Feature engineering for clinical variables
- Ensuring data privacy and HIPAA compliance

Model Selection and Validation
Choosing appropriate algorithms depends on the specific healthcare use case. For diagnostic tasks, consider ensemble methods like Random Forest or Gradient Boosting. For time-series analysis of patient vitals, LSTM networks show promising results.

Cross-validation strategies should account for temporal dependencies and patient-level splitting to avoid data leakage.

Deployment and Monitoring
Healthcare ML models require continuous monitoring for model drift and performance degradation. Implement robust A/B testing frameworks and maintain audit trails for regulatory compliance.'''
        },
        {
            'name': 'software_architecture.txt',
            'content': '''Software Architecture Patterns for Scalable Systems

Overview
This document explores architectural patterns essential for building scalable, maintainable software systems. We'll cover microservices, event-driven architecture, and cloud-native design principles.

Microservices Architecture
Microservices decompose applications into small, independent services that communicate via APIs. Benefits include:
- Independent deployment and scaling
- Technology diversity
- Fault isolation
- Team autonomy

However, microservices introduce complexity in service communication, data consistency, and testing.

Event-Driven Architecture
Event-driven systems use events to trigger and communicate between decoupled application components. This pattern is excellent for real-time systems and complex workflows.

Cloud-Native Design
Cloud-native applications are built specifically for cloud environments, leveraging containerization, orchestration, and managed services for optimal scalability and resilience.'''
        }
    ]
    
    # Create sample documents
    for doc in sample_docs:
        with open(doc['name'], 'w') as f:
            f.write(doc['content'])
    
    # Define sample persona
    persona = {
        'role': 'Data Scientist',
        'experience_level': 'Senior',
        'domain': 'Healthcare',
        'goals': ['machine learning', 'data analysis', 'best practices']
    }
    
    job_to_be_done = "Find best practices for implementing machine learning models in healthcare data analysis"
    
    # Analyze documents
    analyzer = DocumentAnalyst()
    results = analyzer.analyze_documents(
        document_paths=[doc['name'] for doc in sample_docs],
        persona=persona,
        job_to_be_done=job_to_be_done,
        top_k=5
    )
    
    # Display results
    click.echo("Demo Analysis Results:\n")
    for i, result in enumerate(results, 1):
        click.echo(f"{i}. Document: {result['document']}")
        click.echo(f"   Section: {result.get('title', 'Untitled')}")
        click.echo(f"   Relevance Score: {result['score']:.3f}")
        click.echo(f"   Content: {result['content'][:300]}...")
        if i < len(results):
            click.echo("-" * 60)
    
    # Clean up sample files
    for doc in sample_docs:
        try:
            Path(doc['name']).unlink()
        except:
            pass


if __name__ == '__main__':
    cli()