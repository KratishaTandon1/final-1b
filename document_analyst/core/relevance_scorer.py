"""
Relevance Scorer Module
Scores document sections based on persona profile and job requirements.
"""

from typing import Dict, Any, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class RelevanceScorer:
    """Scores document sections for relevance to persona and job."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the relevance scorer.
        
        Args:
            config (dict): Configuration parameters
        """
        self.config = config or {}
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 3),
            min_df=1,
            max_df=0.95
        )
    
    def score_sections(self, sections: List[Dict[str, Any]], persona_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Score document sections based on persona profile.
        
        Args:
            sections (list): List of document sections
            persona_profile (dict): Persona analysis profile
            
        Returns:
            list: Sections with relevance scores
        """
        if not sections:
            return []
        
        # Extract text content from sections
        section_texts = [section.get('content', '') for section in sections]
        
        # Calculate TF-IDF scores
        tfidf_scores = self._calculate_tfidf_scores(section_texts, persona_profile)
        
        # Calculate keyword match scores
        keyword_scores = self._calculate_keyword_scores(sections, persona_profile)
        
        # Calculate semantic similarity scores
        semantic_scores = self._calculate_semantic_scores(sections, persona_profile)
        
        # Combine scores with weights
        final_scores = self._combine_scores(tfidf_scores, keyword_scores, semantic_scores)
        
        # Add scores to sections
        scored_sections = []
        for i, section in enumerate(sections):
            scored_section = section.copy()
            scored_section['score'] = final_scores[i]
            scored_section['score_breakdown'] = {
                'tfidf': tfidf_scores[i],
                'keyword': keyword_scores[i],
                'semantic': semantic_scores[i]
            }
            scored_sections.append(scored_section)
        
        return scored_sections
    
    def _calculate_tfidf_scores(self, section_texts: List[str], persona_profile: Dict[str, Any]) -> List[float]:
        """Calculate TF-IDF based relevance scores."""
        if not section_texts:
            return []
        
        # Create query from persona keywords
        query = ' '.join(persona_profile['keywords'])
        
        # Combine section texts with query for TF-IDF
        all_texts = section_texts + [query]
        
        try:
            # Fit TF-IDF vectorizer
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            
            # Get query vector (last item)
            query_vector = tfidf_matrix[-1]
            
            # Get section vectors
            section_vectors = tfidf_matrix[:-1]
            
            # Calculate cosine similarity
            similarities = cosine_similarity(section_vectors, query_vector).flatten()
            
            return similarities.tolist()
        
        except ValueError:
            # Fallback if TF-IDF fails (e.g., empty texts)
            return [0.0] * len(section_texts)
    
    def _calculate_keyword_scores(self, sections: List[Dict[str, Any]], persona_profile: Dict[str, Any]) -> List[float]:
        """Calculate keyword-based relevance scores."""
        scores = []
        keywords = persona_profile['keywords']
        weights = persona_profile['weights']
        
        for section in sections:
            content = section.get('content', '').lower()
            title = section.get('title', '').lower()
            
            score = 0.0
            total_weight = 0.0
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                weight = weights.get(keyword, 1.0)
                
                # Count occurrences in content and title
                content_matches = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', content))
                title_matches = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', title))
                
                # Title matches get higher weight
                keyword_score = content_matches + (title_matches * 2)
                
                if keyword_score > 0:
                    score += keyword_score * weight
                    total_weight += weight
            
            # Normalize score
            if total_weight > 0:
                scores.append(score / total_weight)
            else:
                scores.append(0.0)
        
        return scores
    
    def _calculate_semantic_scores(self, sections: List[Dict[str, Any]], persona_profile: Dict[str, Any]) -> List[float]:
        """Calculate semantic similarity scores."""
        # For now, use a simple approach based on domain and role matching
        scores = []
        
        persona = persona_profile['persona']
        job_description = persona_profile['job_to_be_done'].lower()
        domain = persona.get('domain', '').lower()
        role = persona.get('role', '').lower()
        
        for section in sections:
            content = section.get('content', '').lower()
            title = section.get('title', '').lower()
            
            score = 0.0
            
            # Check for domain relevance
            if domain and domain in (content + ' ' + title):
                score += 0.3
            
            # Check for role relevance
            if role and any(role_word in (content + ' ' + title) for role_word in role.split()):
                score += 0.2
            
            # Check for job description word overlap
            job_words = set(job_description.split())
            content_words = set((content + ' ' + title).split())
            overlap = len(job_words.intersection(content_words))
            
            if len(job_words) > 0:
                score += (overlap / len(job_words)) * 0.5
            
            scores.append(min(score, 1.0))  # Cap at 1.0
        
        return scores
    
    def _combine_scores(self, tfidf_scores: List[float], keyword_scores: List[float], semantic_scores: List[float]) -> List[float]:
        """Combine different scoring methods with weights."""
        if not tfidf_scores:
            return []
        
        # Score weights (can be configured)
        tfidf_weight = self.config.get('tfidf_weight', 0.4)
        keyword_weight = self.config.get('keyword_weight', 0.4)
        semantic_weight = self.config.get('semantic_weight', 0.2)
        
        # Normalize individual scores to 0-1 range
        tfidf_normalized = self._normalize_scores(tfidf_scores)
        keyword_normalized = self._normalize_scores(keyword_scores)
        semantic_normalized = self._normalize_scores(semantic_scores)
        
        # Combine scores
        final_scores = []
        for i in range(len(tfidf_scores)):
            combined_score = (
                tfidf_normalized[i] * tfidf_weight +
                keyword_normalized[i] * keyword_weight +
                semantic_normalized[i] * semantic_weight
            )
            final_scores.append(combined_score)
        
        return final_scores
    
    def _normalize_scores(self, scores: List[float]) -> List[float]:
        """Normalize scores to 0-1 range."""
        if not scores:
            return []
        
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            return [0.5] * len(scores)  # All scores are the same
        
        normalized = [(score - min_score) / (max_score - min_score) for score in scores]
        return normalized
