"""
Intelligent Document Analyst
A system for extracting and prioritizing relevant document sections based on persona and job-to-be-done.
"""

from .core.document_processor import DocumentProcessor
from .core.persona_analyzer import PersonaAnalyzer
from .core.relevance_scorer import RelevanceScorer

__version__ = "1.0.0"
__author__ = "Document Analyst Team"

class DocumentAnalyst:
    """Main class for the Document Analyst system."""
    
    def __init__(self, config=None):
        """
        Initialize the Document Analyst.
        
        Args:
            config (dict, optional): Configuration parameters
        """
        self.config = config or {}
        self.document_processor = DocumentProcessor(self.config)
        self.persona_analyzer = PersonaAnalyzer(self.config)
        self.relevance_scorer = RelevanceScorer(self.config)
    
    def analyze_documents(self, document_paths, persona, job_to_be_done, top_k=10, enhanced_output=False):
        """
        Analyze documents and return prioritized relevant sections.
        
        Args:
            document_paths (list): List of paths to documents
            persona (dict): Persona information
            job_to_be_done (str): Description of the job to be done
            top_k (int): Number of top results to return
            enhanced_output (bool): Whether to return enhanced output format
            
        Returns:
            list or dict: Prioritized list of relevant document sections or enhanced output
        """
        # Process documents and extract sections
        all_sections = []
        for doc_path in document_paths:
            sections = self.document_processor.process_document(doc_path)
            for section in sections:
                section['document'] = doc_path
                all_sections.append(section)
        
        # Analyze persona and job requirements
        persona_profile = self.persona_analyzer.analyze_persona(persona, job_to_be_done)
        
        # Score sections for relevance
        scored_sections = self.relevance_scorer.score_sections(all_sections, persona_profile)
        
        # Sort by relevance score and return top k
        scored_sections.sort(key=lambda x: x['score'], reverse=True)
        top_sections = scored_sections[:top_k]
        
        if enhanced_output:
            # Use enhanced output formatter
            from enhanced_output_formatter import EnhancedOutputFormatter
            formatter = EnhancedOutputFormatter()
            return formatter.format_analysis_results(
                input_documents=document_paths,
                persona=persona,
                job_to_be_done=job_to_be_done,
                analyzed_sections=top_sections
            )
        else:
            return top_sections
