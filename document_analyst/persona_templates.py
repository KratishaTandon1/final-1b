"""
Enhanced Persona Templates for diverse use cases.
"""

class PersonaTemplates:
    """Pre-defined persona templates for various domains and roles."""
    
    ACADEMIC_RESEARCHER = {
        'role': 'Academic Researcher',
        'experience_level': 'PhD',
        'domain': 'Research',
        'goals': ['literature review', 'research methodology', 'citation analysis', 'theoretical frameworks'],
        'keywords': ['study', 'analysis', 'methodology', 'findings', 'hypothesis', 'experiment', 'theory'],
        'context_preferences': ['abstract', 'introduction', 'methodology', 'results', 'conclusion', 'references']
    }
    
    STUDENT = {
        'role': 'Student',
        'experience_level': 'Undergraduate',
        'domain': 'Education',
        'goals': ['exam preparation', 'concept understanding', 'assignment completion', 'study materials'],
        'keywords': ['definition', 'example', 'explanation', 'formula', 'concept', 'principle', 'theory'],
        'context_preferences': ['examples', 'exercises', 'summaries', 'key concepts', 'definitions']
    }
    
    FINANCIAL_ANALYST = {
        'role': 'Financial Analyst',
        'experience_level': 'Senior',
        'domain': 'Finance',
        'goals': ['financial analysis', 'risk assessment', 'investment decisions', 'market trends'],
        'keywords': ['revenue', 'profit', 'loss', 'assets', 'liabilities', 'cash flow', 'ROI', 'valuation'],
        'context_preferences': ['financial statements', 'executive summary', 'market analysis', 'risk factors']
    }
    
    SALES_PROFESSIONAL = {
        'role': 'Sales Professional',
        'experience_level': 'Senior',
        'domain': 'Sales & Marketing',
        'goals': ['lead generation', 'client presentations', 'competitive analysis', 'market insights'],
        'keywords': ['customer', 'market', 'competition', 'price', 'value proposition', 'benefits'],
        'context_preferences': ['executive summary', 'market overview', 'competitive landscape', 'recommendations']
    }
    
    JOURNALIST = {
        'role': 'Journalist',
        'experience_level': 'Senior',
        'domain': 'Media & Communications',
        'goals': ['story development', 'fact checking', 'source verification', 'trend analysis'],
        'keywords': ['news', 'events', 'people', 'timeline', 'impact', 'quotes', 'sources'],
        'context_preferences': ['headlines', 'key facts', 'quotes', 'timeline', 'impact analysis']
    }
    
    ENTREPRENEUR = {
        'role': 'Entrepreneur',
        'experience_level': 'Experienced',
        'domain': 'Business',
        'goals': ['market opportunity', 'business strategy', 'competitive analysis', 'investment planning'],
        'keywords': ['market', 'opportunity', 'strategy', 'innovation', 'growth', 'scalability', 'funding'],
        'context_preferences': ['market analysis', 'business model', 'financial projections', 'risk assessment']
    }
    
    POLICY_MAKER = {
        'role': 'Policy Maker',
        'experience_level': 'Senior',
        'domain': 'Government & Policy',
        'goals': ['policy analysis', 'impact assessment', 'stakeholder analysis', 'regulatory compliance'],
        'keywords': ['regulation', 'policy', 'compliance', 'impact', 'stakeholders', 'governance'],
        'context_preferences': ['executive summary', 'policy implications', 'stakeholder impact', 'recommendations']
    }
    
    MEDICAL_PROFESSIONAL = {
        'role': 'Medical Professional',
        'experience_level': 'Attending Physician',
        'domain': 'Healthcare',
        'goals': ['clinical guidelines', 'treatment protocols', 'patient care', 'medical research'],
        'keywords': ['patient', 'treatment', 'diagnosis', 'clinical', 'therapy', 'outcomes', 'safety'],
        'context_preferences': ['clinical findings', 'treatment recommendations', 'patient outcomes', 'safety data']
    }
    
    LEGAL_PROFESSIONAL = {
        'role': 'Legal Professional',
        'experience_level': 'Senior Associate',
        'domain': 'Legal',
        'goals': ['case research', 'legal precedents', 'contract analysis', 'compliance review'],
        'keywords': ['law', 'regulation', 'contract', 'liability', 'compliance', 'precedent', 'jurisdiction'],
        'context_preferences': ['legal analysis', 'precedents', 'regulatory requirements', 'risk assessment']
    }
    
    TECHNICAL_WRITER = {
        'role': 'Technical Writer',
        'experience_level': 'Senior',
        'domain': 'Documentation',
        'goals': ['documentation creation', 'technical accuracy', 'user guidance', 'process documentation'],
        'keywords': ['procedure', 'instruction', 'specification', 'guidelines', 'standards', 'process'],
        'context_preferences': ['procedures', 'specifications', 'examples', 'best practices', 'troubleshooting']
    }
    
    @classmethod
    def get_template(cls, role_type: str):
        """Get a persona template by role type."""
        templates = {
            'researcher': cls.ACADEMIC_RESEARCHER,
            'student': cls.STUDENT,
            'financial_analyst': cls.FINANCIAL_ANALYST,
            'sales': cls.SALES_PROFESSIONAL,
            'journalist': cls.JOURNALIST,
            'entrepreneur': cls.ENTREPRENEUR,
            'policy_maker': cls.POLICY_MAKER,
            'medical': cls.MEDICAL_PROFESSIONAL,
            'legal': cls.LEGAL_PROFESSIONAL,
            'technical_writer': cls.TECHNICAL_WRITER,
        }
        return templates.get(role_type.lower())
    
    @classmethod
    def list_available_templates(cls):
        """List all available persona templates."""
        return [
            'researcher', 'student', 'financial_analyst', 'sales',
            'journalist', 'entrepreneur', 'policy_maker', 'medical',
            'legal', 'technical_writer'
        ]
