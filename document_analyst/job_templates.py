"""
Job-to-be-Done templates for various scenarios and personas.
"""

class JobTemplates:
    """Pre-defined job-to-be-done templates for various use cases."""
    
    ACADEMIC_JOBS = {
        'literature_review': {
            'description': 'Conduct a comprehensive literature review on {topic} from available research papers',
            'keywords': ['literature', 'review', 'research', 'papers', 'studies', 'findings', 'methodology'],
            'focus_areas': ['methodology', 'findings', 'conclusions', 'future work', 'related work']
        },
        'research_gap_analysis': {
            'description': 'Identify research gaps and opportunities in {topic} based on current literature',
            'keywords': ['gap', 'opportunity', 'future research', 'limitations', 'unexplored'],
            'focus_areas': ['limitations', 'future work', 'discussion', 'conclusions']
        },
        'methodology_comparison': {
            'description': 'Compare different methodologies and approaches used in {topic} research',
            'keywords': ['methodology', 'approach', 'comparison', 'evaluation', 'techniques'],
            'focus_areas': ['methodology', 'experimental design', 'evaluation', 'results']
        }
    }
    
    EDUCATIONAL_JOBS = {
        'exam_preparation': {
            'description': 'Prepare for {exam_type} exam on {subject} using available study materials',
            'keywords': ['exam', 'study', 'preparation', 'review', 'practice', 'concepts'],
            'focus_areas': ['key concepts', 'examples', 'exercises', 'summaries', 'definitions']
        },
        'concept_understanding': {
            'description': 'Understand key concepts and principles in {subject} for academic coursework',
            'keywords': ['concept', 'principle', 'theory', 'explanation', 'understanding'],
            'focus_areas': ['definitions', 'examples', 'applications', 'explanations']
        },
        'assignment_research': {
            'description': 'Research information for assignment on {topic} using course materials',
            'keywords': ['assignment', 'research', 'information', 'sources', 'evidence'],
            'focus_areas': ['relevant information', 'examples', 'case studies', 'data']
        }
    }
    
    BUSINESS_JOBS = {
        'financial_analysis': {
            'description': 'Analyze financial performance and health of {company} from financial reports',
            'keywords': ['financial', 'analysis', 'performance', 'revenue', 'profit', 'metrics'],
            'focus_areas': ['financial statements', 'key metrics', 'trends', 'risk factors']
        },
        'market_research': {
            'description': 'Research market trends and opportunities in {industry} sector',
            'keywords': ['market', 'trends', 'opportunities', 'competition', 'growth'],
            'focus_areas': ['market analysis', 'competitive landscape', 'trends', 'forecasts']
        },
        'competitive_analysis': {
            'description': 'Analyze competitors and competitive landscape in {industry}',
            'keywords': ['competitive', 'analysis', 'competitors', 'market share', 'strategy'],
            'focus_areas': ['competitive overview', 'market position', 'strengths', 'weaknesses']
        }
    }
    
    JOURNALISM_JOBS = {
        'story_research': {
            'description': 'Research background information for story on {topic}',
            'keywords': ['story', 'research', 'background', 'facts', 'sources', 'context'],
            'focus_areas': ['key facts', 'timeline', 'stakeholders', 'impact']
        },
        'fact_checking': {
            'description': 'Verify facts and claims related to {topic} using reliable sources',
            'keywords': ['fact', 'verification', 'claims', 'sources', 'accuracy'],
            'focus_areas': ['factual information', 'sources', 'verification', 'evidence']
        },
        'trend_analysis': {
            'description': 'Analyze trends and patterns in {domain} for news coverage',
            'keywords': ['trends', 'patterns', 'analysis', 'developments', 'changes'],
            'focus_areas': ['trend data', 'analysis', 'implications', 'expert opinions']
        }
    }
    
    LEGAL_JOBS = {
        'case_research': {
            'description': 'Research legal precedents and case law related to {legal_issue}',
            'keywords': ['case', 'precedent', 'law', 'legal', 'court', 'ruling'],
            'focus_areas': ['legal precedents', 'court decisions', 'legal analysis', 'implications']
        },
        'contract_analysis': {
            'description': 'Analyze contract terms and legal implications for {contract_type}',
            'keywords': ['contract', 'terms', 'legal', 'obligations', 'liability'],
            'focus_areas': ['contract terms', 'legal obligations', 'risk assessment', 'compliance']
        },
        'regulatory_compliance': {
            'description': 'Ensure compliance with regulations in {industry} sector',
            'keywords': ['regulatory', 'compliance', 'regulations', 'requirements', 'standards'],
            'focus_areas': ['regulatory requirements', 'compliance standards', 'penalties', 'procedures']
        }
    }
    
    MEDICAL_JOBS = {
        'clinical_guidelines': {
            'description': 'Find clinical guidelines and best practices for treating {condition}',
            'keywords': ['clinical', 'guidelines', 'treatment', 'best practices', 'protocols'],
            'focus_areas': ['treatment protocols', 'clinical guidelines', 'best practices', 'outcomes']
        },
        'treatment_research': {
            'description': 'Research latest treatment options and efficacy for {medical_condition}',
            'keywords': ['treatment', 'therapy', 'efficacy', 'outcomes', 'clinical trials'],
            'focus_areas': ['treatment options', 'clinical trials', 'efficacy data', 'side effects']
        },
        'diagnostic_criteria': {
            'description': 'Understand diagnostic criteria and procedures for {condition}',
            'keywords': ['diagnostic', 'criteria', 'symptoms', 'tests', 'procedures'],
            'focus_areas': ['diagnostic criteria', 'symptoms', 'test procedures', 'differential diagnosis']
        }
    }
    
    @classmethod
    def get_jobs_for_domain(cls, domain: str):
        """Get job templates for a specific domain."""
        domain_mapping = {
            'academic': cls.ACADEMIC_JOBS,
            'education': cls.EDUCATIONAL_JOBS,
            'business': cls.BUSINESS_JOBS,
            'finance': cls.BUSINESS_JOBS,
            'journalism': cls.JOURNALISM_JOBS,
            'media': cls.JOURNALISM_JOBS,
            'legal': cls.LEGAL_JOBS,
            'medical': cls.MEDICAL_JOBS,
            'healthcare': cls.MEDICAL_JOBS,
        }
        return domain_mapping.get(domain.lower(), {})
    
    @classmethod
    def suggest_job_for_persona(cls, persona_role: str, domain: str = None):
        """Suggest appropriate jobs for a given persona."""
        role_lower = persona_role.lower()
        
        if 'researcher' in role_lower or 'academic' in role_lower:
            return cls.ACADEMIC_JOBS
        elif 'student' in role_lower:
            return cls.EDUCATIONAL_JOBS
        elif any(term in role_lower for term in ['analyst', 'business', 'financial', 'sales', 'entrepreneur']):
            return cls.BUSINESS_JOBS
        elif 'journalist' in role_lower or 'reporter' in role_lower:
            return cls.JOURNALISM_JOBS
        elif 'legal' in role_lower or 'lawyer' in role_lower:
            return cls.LEGAL_JOBS
        elif any(term in role_lower for term in ['medical', 'doctor', 'physician', 'nurse']):
            return cls.MEDICAL_JOBS
        else:
            # Default to business jobs for unknown roles
            return cls.BUSINESS_JOBS
