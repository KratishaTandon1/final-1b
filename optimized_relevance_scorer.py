"""
Optimized Relevance Scorer for Challenge Scoring Criteria
Focuses on Section Relevance (60 points) and Sub-Section Relevance (40 points)
"""

import re
import math
from typing import Dict, List, Tuple, Any
from collections import Counter, defaultdict


class OptimizedRelevanceScorer:
    """Enhanced relevance scorer optimized for challenge scoring criteria."""
    
    def __init__(self):
        self.section_weight = 0.6  # 60% of score
        self.subsection_weight = 0.4  # 40% of score
        
    def calculate_enhanced_relevance_score(self, 
                                         document_content: str,
                                         persona: Dict[str, Any], 
                                         job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive relevance score optimized for scoring criteria.
        
        Returns:
            Dict containing section scores, subsection scores, and overall ranking
        """
        # Extract sections and subsections
        sections = self._extract_sections(document_content)
        
        # Calculate section-level relevance (60 points focus)
        section_scores = self._calculate_section_relevance(sections, persona, job)
        
        # Calculate subsection-level relevance (40 points focus)
        subsection_scores = self._calculate_subsection_relevance(sections, persona, job)
        
        # Create comprehensive ranking
        overall_ranking = self._create_stack_ranking(section_scores, subsection_scores)
        
        return {
            'section_scores': section_scores,
            'subsection_scores': subsection_scores,
            'overall_ranking': overall_ranking,
            'total_score': self._calculate_weighted_score(section_scores, subsection_scores),
            'scoring_breakdown': {
                'section_relevance_contribution': self.section_weight,
                'subsection_relevance_contribution': self.subsection_weight
            }
        }
    
    def _extract_sections(self, content: str) -> List[Dict[str, Any]]:
        """Extract structured sections and subsections from document content."""
        sections = []
        
        # Split content by common section patterns
        section_patterns = [
            r'\n\s*([A-Z][A-Za-z\s]+:)\s*\n',  # "Section Name:"
            r'\n\s*(\d+\.?\s+[A-Za-z][^.\n]+)\s*\n',  # "1. Section Name"
            r'\n\s*([A-Z][A-Z\s]+)\s*\n',  # "ALL CAPS SECTIONS"
            r'\n\s*([A-Za-z][^.\n]{10,50})\s*\n\s*\n',  # Standalone lines
        ]
        
        current_section = {"title": "Introduction", "content": "", "subsections": []}
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Check if this line is a section header
            is_section_header = False
            for pattern in section_patterns:
                if re.match(pattern, f'\n{line}\n'):
                    is_section_header = True
                    break
            
            if is_section_header and current_section["content"]:
                # Save current section and start new one
                current_section["subsections"] = self._extract_subsections(current_section["content"])
                sections.append(current_section)
                current_section = {"title": line, "content": "", "subsections": []}
            else:
                # Add to current section content
                current_section["content"] += line + " "
        
        # Add the last section
        if current_section["content"]:
            current_section["subsections"] = self._extract_subsections(current_section["content"])
            sections.append(current_section)
        
        return sections
    
    def _extract_subsections(self, content: str) -> List[Dict[str, str]]:
        """Extract subsections from section content."""
        subsections = []
        
        # Split by sentences and group related sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Group sentences into subsections (3-5 sentences per subsection)
        subsection_size = 3
        for i in range(0, len(sentences), subsection_size):
            subsection_content = '. '.join(sentences[i:i+subsection_size])
            if subsection_content:
                subsections.append({
                    'title': f'Subsection {i//subsection_size + 1}',
                    'content': subsection_content,
                    'sentence_count': min(subsection_size, len(sentences) - i)
                })
        
        return subsections
    
    def _calculate_section_relevance(self, sections: List[Dict[str, Any]], 
                                   persona: Dict[str, Any], 
                                   job: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate section-level relevance scores (60% of total score)."""
        persona_keywords = self._extract_persona_keywords(persona)
        job_keywords = self._extract_job_keywords(job)
        
        section_scores = []
        
        for section in sections:
            # Calculate multiple relevance factors
            keyword_match_score = self._calculate_keyword_match(
                section['content'], persona_keywords + job_keywords
            )
            
            context_relevance_score = self._calculate_context_relevance(
                section['content'], persona, job
            )
            
            content_quality_score = self._calculate_content_quality(section['content'])
            
            # Weighted combination for section relevance
            total_score = (
                keyword_match_score * 0.4 +
                context_relevance_score * 0.4 +
                content_quality_score * 0.2
            )
            
            section_scores.append({
                'title': section['title'],
                'content': section['content'][:200] + '...' if len(section['content']) > 200 else section['content'],
                'relevance_score': total_score,
                'keyword_match': keyword_match_score,
                'context_relevance': context_relevance_score,
                'content_quality': content_quality_score,
                'subsection_count': len(section['subsections'])
            })
        
        # Sort by relevance score (stack ranking)
        section_scores.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Add ranking position
        for i, section in enumerate(section_scores):
            section['rank'] = i + 1
        
        return section_scores
    
    def _calculate_subsection_relevance(self, sections: List[Dict[str, Any]], 
                                      persona: Dict[str, Any], 
                                      job: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate subsection-level relevance scores (40% of total score)."""
        persona_keywords = self._extract_persona_keywords(persona)
        job_keywords = self._extract_job_keywords(job)
        
        all_subsections = []
        
        for section in sections:
            for subsection in section['subsections']:
                # Calculate granular relevance factors
                keyword_density = self._calculate_keyword_density(
                    subsection['content'], persona_keywords + job_keywords
                )
                
                specificity_score = self._calculate_specificity_score(
                    subsection['content'], persona, job
                )
                
                actionability_score = self._calculate_actionability_score(
                    subsection['content'], job
                )
                
                # Weighted combination for subsection relevance
                total_score = (
                    keyword_density * 0.35 +
                    specificity_score * 0.35 +
                    actionability_score * 0.3
                )
                
                all_subsections.append({
                    'parent_section': section['title'],
                    'title': subsection['title'],
                    'content': subsection['content'],
                    'relevance_score': total_score,
                    'keyword_density': keyword_density,
                    'specificity_score': specificity_score,
                    'actionability_score': actionability_score,
                    'sentence_count': subsection['sentence_count']
                })
        
        # Sort by relevance score (granular ranking)
        all_subsections.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Add ranking position
        for i, subsection in enumerate(all_subsections):
            subsection['rank'] = i + 1
        
        return all_subsections
    
    def _extract_persona_keywords(self, persona: Dict[str, Any]) -> List[str]:
        """Extract relevant keywords from persona definition."""
        keywords = []
        
        # Extract from different persona fields
        for field in ['goals', 'keywords', 'role', 'domain', 'context_preferences']:
            if field in persona:
                if isinstance(persona[field], list):
                    keywords.extend(persona[field])
                elif isinstance(persona[field], str):
                    keywords.append(persona[field])
        
        # Add role-specific keywords
        role = persona.get('role', '').lower()
        if 'travel' in role:
            keywords.extend(['destination', 'itinerary', 'accommodation', 'activities'])
        elif 'hr' in role:
            keywords.extend(['forms', 'onboarding', 'compliance', 'documentation'])
        elif 'food' in role or 'contractor' in role:
            keywords.extend(['menu', 'ingredients', 'recipes', 'dietary'])
        
        return [k.lower() for k in keywords if k]
    
    def _extract_job_keywords(self, job: Dict[str, Any]) -> List[str]:
        """Extract relevant keywords from job definition."""
        keywords = []
        
        # Extract from job description
        if 'description' in job:
            description = job['description'].lower()
            keywords.extend(re.findall(r'\b[a-z]{3,}\b', description))
        
        # Extract from job-specific fields
        for field in ['keywords', 'focus_areas', 'requirements']:
            if field in job:
                if isinstance(job[field], list):
                    keywords.extend(job[field])
                elif isinstance(job[field], str):
                    keywords.append(job[field])
        
        return [k.lower() for k in keywords if k]
    
    def _calculate_keyword_match(self, content: str, keywords: List[str]) -> float:
        """Calculate keyword matching score."""
        content_lower = content.lower()
        matches = sum(1 for keyword in keywords if keyword in content_lower)
        return min(matches / max(len(keywords), 1), 1.0)
    
    def _calculate_keyword_density(self, content: str, keywords: List[str]) -> float:
        """Calculate keyword density for granular analysis."""
        words = re.findall(r'\b\w+\b', content.lower())
        if not words:
            return 0.0
        
        keyword_count = sum(1 for word in words if word in keywords)
        return min(keyword_count / len(words), 0.3)  # Cap at 30% density
    
    def _calculate_context_relevance(self, content: str, persona: Dict[str, Any], job: Dict[str, Any]) -> float:
        """Calculate contextual relevance beyond keyword matching."""
        score = 0.0
        content_lower = content.lower()
        
        # Check for persona context preferences
        context_prefs = persona.get('context_preferences', [])
        for pref in context_prefs:
            if pref.lower() in content_lower:
                score += 0.1
        
        # Check for job focus areas
        focus_areas = job.get('focus_areas', [])
        for area in focus_areas:
            if area.lower() in content_lower:
                score += 0.15
        
        return min(score, 1.0)
    
    def _calculate_specificity_score(self, content: str, persona: Dict[str, Any], job: Dict[str, Any]) -> float:
        """Calculate how specific the content is to the persona and job."""
        score = 0.0
        
        # Look for specific terms, numbers, and detailed information
        specific_patterns = [
            r'\d+\s*(days?|hours?|minutes?)',  # Time specifics
            r'\$\d+|\d+\s*%',  # Money or percentages
            r'\b\d+\s*(people|person|guests?)\b',  # Group size
            r'\b(step\s*\d+|instruction|procedure|method)\b',  # Instructions
            r'\b(gluten-free|vegetarian|vegan|dietary)\b',  # Dietary specifics
        ]
        
        for pattern in specific_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_actionability_score(self, content: str, job: Dict[str, Any]) -> float:
        """Calculate how actionable the content is for the job."""
        action_words = [
            'plan', 'create', 'prepare', 'organize', 'implement', 'design',
            'choose', 'select', 'include', 'consider', 'recommend', 'suggest'
        ]
        
        content_lower = content.lower()
        action_count = sum(1 for word in action_words if word in content_lower)
        
        return min(action_count * 0.1, 1.0)
    
    def _calculate_content_quality(self, content: str) -> float:
        """Calculate overall content quality score."""
        # Length factor (optimal length range)
        length_score = min(len(content) / 1000, 1.0) if len(content) < 1000 else max(1000 / len(content), 0.5)
        
        # Information density (avoid repetitive content)
        words = re.findall(r'\b\w+\b', content.lower())
        unique_words = len(set(words))
        diversity_score = unique_words / max(len(words), 1) if words else 0
        
        return (length_score + diversity_score) / 2
    
    def _create_stack_ranking(self, section_scores: List[Dict[str, Any]], 
                            subsection_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create comprehensive stack ranking combining sections and subsections."""
        return {
            'top_sections': section_scores[:10],  # Top 10 sections
            'top_subsections': subsection_scores[:20],  # Top 20 subsections
            'section_ranking_criteria': [
                'keyword_match (40%)',
                'context_relevance (40%)',
                'content_quality (20%)'
            ],
            'subsection_ranking_criteria': [
                'keyword_density (35%)',
                'specificity_score (35%)',
                'actionability_score (30%)'
            ]
        }
    
    def _calculate_weighted_score(self, section_scores: List[Dict[str, Any]], 
                                subsection_scores: List[Dict[str, Any]]) -> float:
        """Calculate final weighted score based on scoring criteria."""
        # Average top section scores (60% weight)
        avg_section_score = sum(s['relevance_score'] for s in section_scores[:5]) / min(5, len(section_scores))
        section_contribution = avg_section_score * self.section_weight
        
        # Average top subsection scores (40% weight)
        avg_subsection_score = sum(s['relevance_score'] for s in subsection_scores[:10]) / min(10, len(subsection_scores))
        subsection_contribution = avg_subsection_score * self.subsection_weight
        
        return section_contribution + subsection_contribution
