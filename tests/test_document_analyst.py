"""
Tests for the Document Analyst system.
"""

import unittest
import tempfile
import os
from pathlib import Path
import json

from document_analyst import DocumentAnalyst
from document_analyst.core.persona_analyzer import PersonaAnalyzer
from document_analyst.core.relevance_scorer import RelevanceScorer
from document_analyst.parsers.txt_parser import TXTParser

class TestDocumentAnalyst(unittest.TestCase):
    """Test cases for the main DocumentAnalyst class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyst = DocumentAnalyst()
        self.sample_persona = {
            "role": "Data Scientist",
            "experience_level": "Senior",
            "domain": "Healthcare",
            "goals": ["machine learning", "data analysis"]
        }
        self.sample_job = "Find machine learning best practices"
    
    def test_initialization(self):
        """Test DocumentAnalyst initialization."""
        self.assertIsNotNone(self.analyst)
        self.assertIsNotNone(self.analyst.document_processor)
        self.assertIsNotNone(self.analyst.persona_analyzer)
        self.assertIsNotNone(self.analyst.relevance_scorer)
    
    def test_analyze_documents_empty_list(self):
        """Test analyzing empty document list."""
        results = self.analyst.analyze_documents(
            document_paths=[],
            persona=self.sample_persona,
            job_to_be_done=self.sample_job
        )
        self.assertEqual(len(results), 0)

class TestPersonaAnalyzer(unittest.TestCase):
    """Test cases for PersonaAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = PersonaAnalyzer()
    
    def test_analyze_persona_basic(self):
        """Test basic persona analysis."""
        persona = {
            "role": "Data Scientist",
            "experience_level": "Senior",
            "domain": "Healthcare"
        }
        job = "Find machine learning best practices"
        
        profile = self.analyzer.analyze_persona(persona, job)
        
        self.assertIn('keywords', profile)
        self.assertIn('weights', profile)
        self.assertIn('machine', profile['keywords'])
        self.assertIn('learning', profile['keywords'])
    
    def test_extract_job_keywords(self):
        """Test job keyword extraction."""
        job = "Find best practices for machine learning in healthcare"
        keywords = self.analyzer._extract_job_keywords(job)
        
        self.assertIn('machine', keywords)
        self.assertIn('learning', keywords)
        self.assertIn('healthcare', keywords)
        self.assertIn('best', keywords)
        self.assertIn('practices', keywords)

class TestRelevanceScorer(unittest.TestCase):
    """Test cases for RelevanceScorer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scorer = RelevanceScorer()
    
    def test_score_sections_empty(self):
        """Test scoring empty sections list."""
        persona_profile = {
            'keywords': ['machine', 'learning'],
            'weights': {'machine': 2.0, 'learning': 2.0}
        }
        
        results = self.scorer.score_sections([], persona_profile)
        self.assertEqual(len(results), 0)
    
    def test_score_sections_basic(self):
        """Test basic section scoring."""
        sections = [
            {
                'content': 'This section discusses machine learning algorithms and data analysis techniques.',
                'title': 'Machine Learning Overview'
            },
            {
                'content': 'This section covers software engineering best practices and coding standards.',
                'title': 'Software Engineering'
            }
        ]
        
        persona_profile = {
            'keywords': ['machine', 'learning', 'data', 'analysis'],
            'weights': {'machine': 2.0, 'learning': 2.0, 'data': 1.5, 'analysis': 1.5},
            'persona': {'role': 'Data Scientist'},
            'job_to_be_done': 'machine learning best practices'
        }
        
        results = self.scorer.score_sections(sections, persona_profile)
        
        self.assertEqual(len(results), 2)
        self.assertGreater(results[0]['score'], results[1]['score'])  # First section should score higher

class TestTXTParser(unittest.TestCase):
    """Test cases for TXT parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = TXTParser()
    
    def test_parse_simple_text(self):
        """Test parsing a simple text file."""
        content = "This is a test document.\nIt has multiple lines.\nAnd some content."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = self.parser.parse(temp_path)
            
            self.assertIn('content', result)
            self.assertIn('metadata', result)
            self.assertEqual(result['file_type'], 'txt')
            self.assertEqual(content, result['content'])
        finally:
            os.unlink(temp_path)
    
    def test_is_supported(self):
        """Test file format support detection."""
        self.assertTrue(self.parser.is_supported('test.txt'))
        self.assertTrue(self.parser.is_supported('test.md'))
        self.assertFalse(self.parser.is_supported('test.pdf'))

class TestIntegration(unittest.TestCase):
    """Integration tests for the full system."""
    
    def test_end_to_end_analysis(self):
        """Test complete end-to-end analysis."""
        # Create temporary test documents
        docs = [
            {
                'name': 'ml_doc.txt',
                'content': '''Machine Learning Best Practices
                
                This document covers best practices for machine learning in healthcare.
                Data preprocessing is crucial for model performance.
                Feature engineering helps improve prediction accuracy.
                Cross-validation ensures robust model evaluation.
                '''
            },
            {
                'name': 'software_doc.txt',
                'content': '''Software Development Guidelines
                
                This document outlines software development best practices.
                Code review processes improve code quality.
                Testing strategies ensure system reliability.
                Documentation helps team collaboration.
                '''
            }
        ]
        
        temp_files = []
        
        try:
            # Create temporary files
            for doc in docs:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                    f.write(doc['content'])
                    temp_files.append(f.name)
            
            # Set up analysis
            analyst = DocumentAnalyst()
            persona = {
                "role": "Data Scientist",
                "experience_level": "Senior",
                "domain": "Healthcare",
                "goals": ["machine learning", "data preprocessing"]
            }
            job = "Find machine learning best practices for healthcare"
            
            # Perform analysis
            results = analyst.analyze_documents(
                document_paths=temp_files,
                persona=persona,
                job_to_be_done=job,
                top_k=3
            )
            
            # Verify results
            self.assertGreater(len(results), 0)
            self.assertIn('score', results[0])
            self.assertIn('content', results[0])
            
            # The ML document should score higher than the software document
            ml_scores = [r['score'] for r in results if 'machine learning' in r['content'].lower()]
            software_scores = [r['score'] for r in results if 'software development' in r['content'].lower()]
            
            if ml_scores and software_scores:
                self.assertGreater(max(ml_scores), max(software_scores))
        
        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass

if __name__ == '__main__':
    unittest.main()
