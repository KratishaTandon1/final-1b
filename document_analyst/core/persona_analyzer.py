"""
Persona Analyzer Module
Analyzes persona information and job-to-be-done to create relevance profiles.
"""

from typing import Dict, Any, List
import re

class PersonaAnalyzer:
    """Analyzes persona and job requirements."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the persona analyzer.
        
        Args:
            config (dict): Configuration parameters
        """
        self.config = config or {}
        
        # Role-based keyword mappings
        self.role_keywords = {
            'data_scientist': ['machine learning', 'statistics', 'python', 'r', 'analytics', 'modeling', 'algorithms'],
            'software_engineer': ['programming', 'development', 'coding', 'architecture', 'frameworks', 'apis'],
            'product_manager': ['strategy', 'roadmap', 'requirements', 'stakeholder', 'market', 'user experience'],
            'researcher': ['methodology', 'analysis', 'findings', 'literature', 'study', 'experimental'],
            'business_analyst': ['requirements', 'process', 'workflow', 'optimization', 'metrics', 'kpi'],
            'healthcare_professional': ['clinical', 'patient', 'treatment', 'diagnosis', 'medical', 'therapeutic']
        }
        
        # Experience level modifiers
        self.experience_modifiers = {
            'junior': ['introduction', 'basics', 'fundamentals', 'getting started', 'tutorial'],
            'senior': ['advanced', 'expert', 'best practices', 'optimization', 'scalability', 'architecture'],
            'lead': ['strategy', 'management', 'team', 'leadership', 'governance', 'standards']
        }
    
    def analyze_persona(self, persona: Dict[str, Any], job_to_be_done: str) -> Dict[str, Any]:
        """
        Analyze persona and job to create a relevance profile.
        
        Args:
            persona (dict): Persona information
            job_to_be_done (str): Description of the job to be done
            
        Returns:
            dict: Persona profile with relevance keywords and weights
        """
        profile = {
            'persona': persona,
            'job_to_be_done': job_to_be_done,
            'keywords': [],
            'weights': {},
            'domain_context': []
        }
        
        # Extract keywords from role
        role = persona.get('role', '').lower().replace(' ', '_')
        if role in self.role_keywords:
            profile['keywords'].extend(self.role_keywords[role])
            # Higher weight for role-specific keywords
            for keyword in self.role_keywords[role]:
                profile['weights'][keyword] = 2.0
        
        # Extract keywords from experience level
        experience = persona.get('experience_level', '').lower()
        if experience in self.experience_modifiers:
            profile['keywords'].extend(self.experience_modifiers[experience])
            # Moderate weight for experience-specific keywords
            for keyword in self.experience_modifiers[experience]:
                profile['weights'][keyword] = 1.5
        
        # Extract keywords from domain
        domain = persona.get('domain', '')
        if domain:
            domain_keywords = self._extract_domain_keywords(domain)
            profile['keywords'].extend(domain_keywords)
            profile['domain_context'].append(domain)
            # High weight for domain keywords
            for keyword in domain_keywords:
                profile['weights'][keyword] = 2.5
        
        # Extract keywords from goals
        goals = persona.get('goals', [])
        if goals:
            profile['keywords'].extend(goals)
            # Very high weight for explicit goals
            for goal in goals:
                profile['weights'][goal] = 3.0
        
        # Extract keywords from job-to-be-done
        job_keywords = self._extract_job_keywords(job_to_be_done)
        profile['keywords'].extend(job_keywords)
        # Highest weight for job-specific keywords
        for keyword in job_keywords:
            profile['weights'][keyword] = 3.5
        
        # Remove duplicates while preserving weights
        profile['keywords'] = list(set(profile['keywords']))
        
        return profile
    
    def _extract_domain_keywords(self, domain: str) -> List[str]:
        """Extract relevant keywords from domain."""
        domain_mappings = {
            'healthcare': ['medical', 'clinical', 'patient', 'treatment', 'diagnosis', 'therapeutic'],
            'finance': ['financial', 'investment', 'risk', 'trading', 'portfolio', 'banking'],
            'technology': ['software', 'system', 'platform', 'digital', 'innovation', 'automation'],
            'manufacturing': ['production', 'quality', 'supply chain', 'operations', 'efficiency'],
            'retail': ['customer', 'sales', 'inventory', 'marketing', 'ecommerce', 'consumer'],
            'education': ['learning', 'curriculum', 'assessment', 'student', 'pedagogy', 'academic']
        }
        
        domain_lower = domain.lower()
        for key, keywords in domain_mappings.items():
            if key in domain_lower:
                return keywords
        
        # If no specific mapping, return domain as keyword
        return [domain.lower()]
    
    def _extract_job_keywords(self, job_description: str) -> List[str]:
        """Extract keywords from job-to-be-done description."""
        # Convert to lowercase and remove punctuation
        job_clean = re.sub(r'[^\w\s]', ' ', job_description.lower())
        
        # Split into words and filter
        words = job_clean.split()
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'them', 'their', 'this', 'that', 'these', 'those'
        }
        
        # Filter out stop words and short words
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        
        # Extract multi-word phrases (bigrams and trigrams)
        phrases = []
        for i in range(len(words) - 1):
            if words[i] not in stop_words and words[i+1] not in stop_words:
                phrases.append(f"{words[i]} {words[i+1]}")
        
        for i in range(len(words) - 2):
            if all(word not in stop_words for word in words[i:i+3]):
                phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
        
        return keywords + phrases
