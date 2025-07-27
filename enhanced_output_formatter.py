"""
Enhanced output format for the Document Analyst system.
Provides comprehensive metadata, section analysis, and sub-section breakdowns.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import json

class EnhancedOutputFormatter:
    """Formats analysis results with comprehensive metadata and section details."""
    
    def __init__(self):
        self.processing_timestamp = datetime.now().isoformat()
    
    def format_analysis_results(self, 
                              input_documents: List[str],
                              persona: Dict[str, Any],
                              job_to_be_done: str,
                              analyzed_sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Format the complete analysis results with enhanced structure.
        
        Args:
            input_documents: List of input document paths
            persona: Persona configuration
            job_to_be_done: Job description
            analyzed_sections: Processed and scored sections
            
        Returns:
            Comprehensive analysis results with metadata and detailed sections
        """
        
        # 1. Metadata Section
        metadata = {
            "input_documents": [
                {
                    "filename": self._extract_filename(doc),
                    "full_path": doc,
                    "file_type": self._get_file_extension(doc),
                    "document_id": f"doc_{i+1}"
                }
                for i, doc in enumerate(input_documents)
            ],
            "persona": {
                "role": persona.get('role', 'Unknown'),
                "experience_level": persona.get('experience_level', 'Not specified'),
                "domain": persona.get('domain', 'General'),
                "goals": persona.get('goals', []),
                "keywords": persona.get('keywords', []),
                "context_preferences": persona.get('context_preferences', [])
            },
            "job_to_be_done": {
                "task_description": job_to_be_done,
                "task_type": self._classify_task_type(job_to_be_done),
                "complexity_level": self._assess_complexity(job_to_be_done)
            },
            "processing_timestamp": self.processing_timestamp,
            "analysis_settings": {
                "total_documents_processed": len(input_documents),
                "total_sections_analyzed": len(analyzed_sections),
                "scoring_method": "hybrid_tfidf_semantic_keyword"
            }
        }
        
        # 2. Extracted Sections with detailed analysis
        extracted_sections = []
        
        for i, section in enumerate(analyzed_sections):
            section_data = {
                "section_id": f"section_{i+1}",
                "document": {
                    "filename": self._extract_filename(section.get('document', '')),
                    "document_id": self._get_document_id(section.get('document', ''), input_documents),
                    "full_path": section.get('document', '')
                },
                "page_number": self._extract_page_number(section),
                "section_title": self._generate_section_title(section),
                "importance_rank": i + 1,
                "relevance_score": round(section.get('score', 0.0), 4),
                "score_breakdown": self._get_score_breakdown(section),
                "content_preview": section.get('content', '')[:200] + "..." if len(section.get('content', '')) > 200 else section.get('content', ''),
                "word_count": len(section.get('content', '').split()),
                "extraction_metadata": {
                    "section_type": section.get('section_type', 'text_section'),
                    "extraction_method": section.get('source', 'automatic'),
                    "confidence_level": self._calculate_confidence(section)
                }
            }
            extracted_sections.append(section_data)
        
        # 3. Sub-section Analysis
        subsection_analysis = []
        
        for i, section in enumerate(analyzed_sections[:5]):  # Top 5 sections for detailed analysis
            subsection_data = {
                "subsection_id": f"subsection_{i+1}",
                "parent_section_id": f"section_{i+1}",
                "document": {
                    "filename": self._extract_filename(section.get('document', '')),
                    "document_id": self._get_document_id(section.get('document', ''), input_documents),
                    "source_type": self._get_document_type(section.get('document', ''))
                },
                "refined_text": self._refine_text_content(section.get('content', '')),
                "page_number_constraints": {
                    "start_page": self._extract_page_number(section),
                    "end_page": self._extract_page_number(section),  # Could be enhanced for multi-page sections
                    "page_range": f"Page {self._extract_page_number(section)}",
                    "total_pages_covered": 1
                },
                "content_analysis": {
                    "key_concepts": self._extract_key_concepts(section.get('content', '')),
                    "domain_relevance": self._assess_domain_relevance(section, persona),
                    "job_alignment": self._assess_job_alignment(section, job_to_be_done),
                    "information_density": self._calculate_information_density(section)
                },
                "quality_metrics": {
                    "readability_score": self._calculate_readability(section.get('content', '')),
                    "completeness": self._assess_completeness(section),
                    "specificity": self._assess_specificity(section, job_to_be_done)
                }
            }
            subsection_analysis.append(subsection_data)
        
        # Complete result structure
        complete_results = {
            "analysis_id": f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "metadata": metadata,
            "extracted_sections": extracted_sections,
            "subsection_analysis": subsection_analysis,
            "summary_statistics": {
                "total_sections_found": len(analyzed_sections),
                "average_relevance_score": sum(s.get('score', 0) for s in analyzed_sections) / len(analyzed_sections) if analyzed_sections else 0,
                "highest_scoring_document": self._get_highest_scoring_document(analyzed_sections),
                "content_distribution": self._analyze_content_distribution(analyzed_sections),
                "processing_time_ms": self._estimate_processing_time(len(input_documents), len(analyzed_sections))
            },
            "recommendations": self._generate_recommendations(analyzed_sections, persona, job_to_be_done)
        }
        
        return complete_results
    
    def _extract_filename(self, path: str) -> str:
        """Extract filename from full path."""
        if not path:
            return "Unknown"
        return path.split('\\')[-1].split('/')[-1]
    
    def _get_file_extension(self, path: str) -> str:
        """Get file extension."""
        if '.' in path:
            return path.split('.')[-1].lower()
        return "unknown"
    
    def _get_document_id(self, doc_path: str, all_docs: List[str]) -> str:
        """Get document ID based on position in input list."""
        try:
            index = all_docs.index(doc_path)
            return f"doc_{index + 1}"
        except ValueError:
            return "doc_unknown"
    
    def _extract_page_number(self, section: Dict[str, Any]) -> int:
        """Extract or estimate page number from section."""
        # This could be enhanced based on actual page extraction logic
        section_id = section.get('section_id', 0)
        return max(1, section_id + 1)  # Simple estimation
    
    def _generate_section_title(self, section: Dict[str, Any]) -> str:
        """Generate a meaningful section title."""
        content = section.get('content', '')
        if len(content) > 50:
            # Try to extract first sentence or meaningful phrase
            first_line = content.split('\n')[0].strip()
            if len(first_line) > 5 and len(first_line) < 100:
                return first_line
        return f"Section {section.get('section_id', 'Unknown')}"
    
    def _get_score_breakdown(self, section: Dict[str, Any]) -> Dict[str, float]:
        """Get detailed score breakdown if available."""
        return {
            "total_score": round(section.get('score', 0.0), 4),
            "tfidf_score": round(section.get('tfidf_score', 0.0), 4),
            "keyword_score": round(section.get('keyword_score', 0.0), 4),
            "semantic_score": round(section.get('semantic_score', 0.0), 4)
        }
    
    def _calculate_confidence(self, section: Dict[str, Any]) -> str:
        """Calculate confidence level based on score."""
        score = section.get('score', 0.0)
        if score >= 0.8:
            return "High"
        elif score >= 0.6:
            return "Medium"
        elif score >= 0.4:
            return "Low"
        else:
            return "Very Low"
    
    def _refine_text_content(self, content: str) -> str:
        """Refine and clean text content."""
        # Remove extra whitespace and normalize
        cleaned = ' '.join(content.split())
        
        # Truncate if too long but preserve complete sentences
        if len(cleaned) > 500:
            sentences = cleaned.split('. ')
            refined = ""
            for sentence in sentences:
                if len(refined + sentence) < 450:
                    refined += sentence + ". "
                else:
                    break
            return refined.strip()
        
        return cleaned
    
    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content."""
        # Simple keyword extraction - could be enhanced with NLP
        words = content.lower().split()
        # Filter for meaningful words (longer than 3 chars, not common words)
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'this', 'that', 'from'}
        concepts = []
        
        for word in words:
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 3 and clean_word not in stop_words:
                concepts.append(clean_word)
        
        # Return top 10 most frequent concepts
        from collections import Counter
        concept_counts = Counter(concepts)
        return [concept for concept, count in concept_counts.most_common(10)]
    
    def _assess_domain_relevance(self, section: Dict[str, Any], persona: Dict[str, Any]) -> str:
        """Assess how relevant the section is to the persona's domain."""
        persona_keywords = persona.get('keywords', [])
        content = section.get('content', '').lower()
        
        matches = sum(1 for keyword in persona_keywords if keyword.lower() in content)
        relevance_ratio = matches / max(len(persona_keywords), 1)
        
        if relevance_ratio >= 0.7:
            return "High"
        elif relevance_ratio >= 0.4:
            return "Medium"
        else:
            return "Low"
    
    def _assess_job_alignment(self, section: Dict[str, Any], job_description: str) -> str:
        """Assess how well the section aligns with the job to be done."""
        job_words = set(job_description.lower().split())
        content_words = set(section.get('content', '').lower().split())
        
        overlap = len(job_words.intersection(content_words))
        alignment_ratio = overlap / max(len(job_words), 1)
        
        if alignment_ratio >= 0.3:
            return "High"
        elif alignment_ratio >= 0.15:
            return "Medium"
        else:
            return "Low"
    
    def _calculate_information_density(self, section: Dict[str, Any]) -> str:
        """Calculate information density of the section."""
        content = section.get('content', '')
        words = content.split()
        
        if len(words) == 0:
            return "None"
        
        # Simple heuristic: ratio of unique words to total words
        unique_words = len(set(words))
        density_ratio = unique_words / len(words)
        
        if density_ratio >= 0.7:
            return "High"
        elif density_ratio >= 0.5:
            return "Medium"
        else:
            return "Low"
    
    def _calculate_readability(self, content: str) -> str:
        """Calculate readability score."""
        words = content.split()
        sentences = content.split('.')
        
        if len(sentences) == 0 or len(words) == 0:
            return "Unknown"
        
        avg_words_per_sentence = len(words) / len(sentences)
        
        if avg_words_per_sentence <= 15:
            return "Easy"
        elif avg_words_per_sentence <= 25:
            return "Medium"
        else:
            return "Complex"
    
    def _assess_completeness(self, section: Dict[str, Any]) -> str:
        """Assess completeness of the section."""
        content = section.get('content', '')
        word_count = len(content.split())
        
        if word_count >= 100:
            return "Complete"
        elif word_count >= 50:
            return "Partial"
        else:
            return "Fragment"
    
    def _assess_specificity(self, section: Dict[str, Any], job_description: str) -> str:
        """Assess how specific the section is to the job."""
        content = section.get('content', '').lower()
        job_terms = job_description.lower().split()
        
        specific_matches = sum(1 for term in job_terms if len(term) > 4 and term in content)
        
        if specific_matches >= 3:
            return "High"
        elif specific_matches >= 1:
            return "Medium"
        else:
            return "Low"
    
    def _classify_task_type(self, job_description: str) -> str:
        """Classify the type of task."""
        job_lower = job_description.lower()
        
        if any(word in job_lower for word in ['research', 'literature', 'review', 'analysis']):
            return "Research & Analysis"
        elif any(word in job_lower for word in ['exam', 'study', 'learn', 'understand']):
            return "Learning & Education"
        elif any(word in job_lower for word in ['financial', 'business', 'market', 'investment']):
            return "Business & Finance"
        elif any(word in job_lower for word in ['story', 'news', 'article', 'journalism']):
            return "Journalism & Media"
        elif any(word in job_lower for word in ['legal', 'contract', 'compliance', 'law']):
            return "Legal & Compliance"
        else:
            return "General Task"
    
    def _assess_complexity(self, job_description: str) -> str:
        """Assess the complexity level of the task."""
        complexity_indicators = ['comprehensive', 'detailed', 'thorough', 'systematic', 'complex', 'advanced']
        job_lower = job_description.lower()
        
        if any(indicator in job_lower for indicator in complexity_indicators):
            return "High"
        elif len(job_description.split()) > 10:
            return "Medium"
        else:
            return "Low"
    
    def _get_highest_scoring_document(self, sections: List[Dict[str, Any]]) -> str:
        """Find the document with the highest average score."""
        if not sections:
            return "None"
        
        doc_scores = {}
        for section in sections:
            doc = self._extract_filename(section.get('document', ''))
            score = section.get('score', 0.0)
            
            if doc not in doc_scores:
                doc_scores[doc] = []
            doc_scores[doc].append(score)
        
        # Calculate average scores
        avg_scores = {doc: sum(scores)/len(scores) for doc, scores in doc_scores.items()}
        
        return max(avg_scores, key=avg_scores.get) if avg_scores else "None"
    
    def _analyze_content_distribution(self, sections: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze how content is distributed across documents."""
        distribution = {}
        
        for section in sections:
            doc = self._extract_filename(section.get('document', ''))
            distribution[doc] = distribution.get(doc, 0) + 1
        
        return distribution
    
    def _estimate_processing_time(self, num_docs: int, num_sections: int) -> int:
        """Estimate processing time in milliseconds."""
        # Simple estimation based on document and section count
        base_time = 100  # Base processing time
        doc_time = num_docs * 50  # Time per document
        section_time = num_sections * 10  # Time per section
        
        return base_time + doc_time + section_time
    
    def _get_document_type(self, doc_path: str) -> str:
        """Determine document type based on path or content."""
        filename = self._extract_filename(doc_path).lower()
        
        if 'research' in filename or 'paper' in filename:
            return "Research Paper"
        elif 'report' in filename or 'financial' in filename:
            return "Business Report"
        elif 'textbook' in filename or 'chapter' in filename:
            return "Educational Material"
        elif 'news' in filename or 'article' in filename:
            return "News Article"
        elif 'contract' in filename or 'legal' in filename:
            return "Legal Document"
        else:
            return "General Document"
    
    def _generate_recommendations(self, sections: List[Dict[str, Any]], persona: Dict[str, Any], job_description: str) -> List[str]:
        """Generate recommendations based on analysis results."""
        recommendations = []
        
        if not sections:
            recommendations.append("No relevant sections found. Consider refining the search criteria or adding more documents.")
            return recommendations
        
        avg_score = sum(s.get('score', 0) for s in sections) / len(sections)
        
        if avg_score < 0.3:
            recommendations.append("Low overall relevance scores detected. Consider:")
            recommendations.append("- Refining the persona definition with more specific keywords")
            recommendations.append("- Adjusting the job description to be more specific")
            recommendations.append("- Adding documents more closely related to the task")
        
        if len(sections) < 3:
            recommendations.append("Limited sections found. Consider adding more documents to the collection.")
        
        # Document-specific recommendations
        doc_distribution = self._analyze_content_distribution(sections)
        if len(doc_distribution) == 1:
            recommendations.append("Content found in only one document. Consider diversifying the document collection.")
        
        return recommendations

# Usage example function
def create_enhanced_output_example():
    """Example of how to use the enhanced output formatter."""
    
    formatter = EnhancedOutputFormatter()
    
    # Example inputs
    input_documents = [
        "c:\\Users\\example\\documents\\research_paper.pdf",
        "c:\\Users\\example\\documents\\textbook_chapter.pdf"
    ]
    
    persona = {
        'role': 'Academic Researcher',
        'experience_level': 'PhD',
        'domain': 'Computer Science',
        'goals': ['literature review', 'research methodology'],
        'keywords': ['machine learning', 'algorithms', 'analysis'],
        'context_preferences': ['methodology', 'results', 'conclusions']
    }
    
    job_to_be_done = "Conduct a comprehensive literature review on machine learning algorithms"
    
    # Example analyzed sections (would come from actual analysis)
    analyzed_sections = [
        {
            'content': 'Machine learning algorithms have revolutionized data analysis...',
            'score': 0.95,
            'document': input_documents[0],
            'section_id': 0,
            'tfidf_score': 0.3,
            'keyword_score': 0.4,
            'semantic_score': 0.25
        }
    ]
    
    # Generate enhanced output
    results = formatter.format_analysis_results(
        input_documents=input_documents,
        persona=persona,
        job_to_be_done=job_to_be_done,
        analyzed_sections=analyzed_sections
    )
    
    return results

if __name__ == "__main__":
    # Create example output
    example_results = create_enhanced_output_example()
    
    # Pretty print the results
    print("🎯 ENHANCED OUTPUT FORMAT EXAMPLE")
    print("=" * 80)
    print(json.dumps(example_results, indent=2, ensure_ascii=False))
