"""
Lightweight CPU-Only Document Analyst Configuration
Optimized for performance constraints: CPU-only, ≤1GB memory, ≤60s processing, no internet
"""

import os
import sys
import time
import psutil
from typing import Dict, List, Any, Optional
import json
import pickle
from pathlib import Path
from optimized_relevance_scorer import OptimizedRelevanceScorer

class LightweightConfig:
    """Configuration for CPU-only, lightweight operation."""
    
    # Performance constraints
    MAX_MODEL_SIZE_GB = 1.0
    MAX_PROCESSING_TIME_SECONDS = 60
    MAX_MEMORY_USAGE_GB = 0.9
    CPU_ONLY = True
    NO_INTERNET = True
    
    # Optimization settings
    MAX_DOCUMENT_SIZE_MB = 50  # Limit individual document size
    MAX_SECTIONS_PER_DOC = 20  # Limit sections to process per document
    MAX_CONTENT_LENGTH = 10000  # Limit content length per section
    BATCH_SIZE = 1  # Process documents one at a time
    
    # Lightweight NLP settings
    USE_SIMPLE_TOKENIZER = True
    USE_LIGHTWEIGHT_EMBEDDINGS = True
    DISABLE_COMPLEX_NLP = True
    
    @classmethod
    def validate_system_requirements(cls):
        """Validate system meets requirements."""
        
        # Check available memory
        available_memory_gb = psutil.virtual_memory().available / (1024**3)
        if available_memory_gb < cls.MAX_MEMORY_USAGE_GB:
            raise RuntimeError(f"Insufficient memory. Need {cls.MAX_MEMORY_USAGE_GB}GB, have {available_memory_gb:.2f}GB")
        
        # Check CPU availability
        cpu_count = psutil.cpu_count()
        if cpu_count < 2:
            print(f"Warning: Only {cpu_count} CPU cores available. Performance may be limited.")
        
        print(f"✅ System validation passed:")
        print(f"   • Available Memory: {available_memory_gb:.2f}GB")
        print(f"   • CPU Cores: {cpu_count}")
        print(f"   • Mode: CPU-only, No Internet")
        
        return True

class LightweightTextProcessor:
    """Lightweight text processing without heavy NLP dependencies."""
    
    def __init__(self, config: LightweightConfig):
        self.config = config
        self.stop_words = self._load_simple_stopwords()
        
    def _load_simple_stopwords(self) -> set:
        """Load a simple set of stop words without external dependencies."""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'this', 'that', 'these', 'those', 'is', 'are', 
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 
            'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their'
        }
    
    def simple_tokenize(self, text: str) -> List[str]:
        """Simple tokenization without complex NLP."""
        import re
        
        # Convert to lowercase and extract words
        text = text.lower()
        words = re.findall(r'\b[a-z]{2,}\b', text)
        
        # Filter stop words
        filtered_words = [word for word in words if word not in self.stop_words]
        
        return filtered_words
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """Extract keywords using simple frequency analysis."""
        from collections import Counter
        
        words = self.simple_tokenize(text)
        
        # Count word frequencies
        word_counts = Counter(words)
        
        # Return top k most frequent words
        return [word for word, count in word_counts.most_common(top_k)]
    
    def simple_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple word overlap similarity."""
        words1 = set(self.simple_tokenize(text1))
        words2 = set(self.simple_tokenize(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0

class LightweightDocumentProcessor:
    """Lightweight document processor optimized for performance."""
    
    def __init__(self, config: LightweightConfig):
        self.config = config
        self.text_processor = LightweightTextProcessor(config)
        self.processing_start_time = None
        
    def start_processing_timer(self):
        """Start the processing timer."""
        self.processing_start_time = time.time()
    
    def check_time_limit(self):
        """Check if processing time limit is exceeded."""
        if self.processing_start_time:
            elapsed = time.time() - self.processing_start_time
            if elapsed > self.config.MAX_PROCESSING_TIME_SECONDS:
                raise TimeoutError(f"Processing time limit exceeded: {elapsed:.2f}s > {self.config.MAX_PROCESSING_TIME_SECONDS}s")
    
    def process_document_fast(self, document_path: str) -> List[Dict[str, Any]]:
        """Fast document processing with minimal overhead."""
        
        self.check_time_limit()
        
        # Check file size
        file_size_mb = os.path.getsize(document_path) / (1024 * 1024)
        if file_size_mb > self.config.MAX_DOCUMENT_SIZE_MB:
            print(f"Warning: Document {document_path} is {file_size_mb:.2f}MB, may be slow")
        
        # Simple text extraction
        try:
            if document_path.lower().endswith('.pdf'):
                content = self._extract_pdf_fast(document_path)
            elif document_path.lower().endswith(('.docx', '.doc')):
                content = self._extract_docx_fast(document_path)
            else:
                content = self._extract_txt_fast(document_path)
        except Exception as e:
            print(f"Error processing {document_path}: {e}")
            return []
        
        # Simple section splitting
        sections = self._split_into_sections_fast(content, document_path)
        
        return sections[:self.config.MAX_SECTIONS_PER_DOC]
    
    def _extract_pdf_fast(self, pdf_path: str) -> str:
        """Fast PDF text extraction."""
        try:
            import PyPDF2
            
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Limit pages to process for speed
                max_pages = min(len(reader.pages), 50)
                
                for page_num in range(max_pages):
                    self.check_time_limit()
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text
        except ImportError:
            # Fallback: try basic text extraction
            print("PyPDF2 not available, using basic extraction")
            return self._extract_txt_fast(pdf_path)
    
    def _extract_docx_fast(self, docx_path: str) -> str:
        """Fast DOCX text extraction."""
        try:
            import docx
            
            doc = docx.Document(docx_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                self.check_time_limit()
                text += paragraph.text + "\n"
            
            return text
        except ImportError:
            print("python-docx not available, using basic extraction")
            return self._extract_txt_fast(docx_path)
    
    def _extract_txt_fast(self, txt_path: str) -> str:
        """Fast text file extraction."""
        try:
            with open(txt_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                
                # Limit content length
                if len(content) > self.config.MAX_CONTENT_LENGTH * 10:
                    content = content[:self.config.MAX_CONTENT_LENGTH * 10]
                
                return content
        except Exception as e:
            print(f"Error reading text file: {e}")
            return ""
    
    def _split_into_sections_fast(self, content: str, document_path: str) -> List[Dict[str, Any]]:
        """Fast section splitting using simple heuristics."""
        
        # Simple paragraph-based splitting
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        sections = []
        current_section = ""
        section_id = 0
        
        for paragraph in paragraphs:
            self.check_time_limit()
            
            # Check if this looks like a section header
            if self._is_section_header(paragraph):
                # Save previous section
                if current_section:
                    sections.append(self._create_section_dict(
                        current_section, section_id, document_path
                    ))
                    section_id += 1
                
                # Start new section
                current_section = paragraph + "\n"
            else:
                current_section += paragraph + "\n"
            
            # Limit section length
            if len(current_section) > self.config.MAX_CONTENT_LENGTH:
                sections.append(self._create_section_dict(
                    current_section, section_id, document_path
                ))
                section_id += 1
                current_section = ""
        
        # Add final section
        if current_section:
            sections.append(self._create_section_dict(
                current_section, section_id, document_path
            ))
        
        return sections
    
    def _is_section_header(self, text: str) -> bool:
        """Simple heuristic to detect section headers."""
        text = text.strip()
        
        # Check for common header patterns
        if len(text) > 100:  # Too long to be a header
            return False
        
        # Check for numbering or formatting
        if any(pattern in text.lower() for pattern in [
            'chapter', 'section', 'introduction', 'conclusion', 
            'overview', 'summary', 'abstract', 'methodology'
        ]):
            return True
        
        # Check for title case or all caps
        if text.isupper() or text.istitle():
            return True
        
        return False
    
    def _create_section_dict(self, content: str, section_id: int, document_path: str) -> Dict[str, Any]:
        """Create section dictionary with metadata."""
        
        content = content.strip()
        if len(content) > self.config.MAX_CONTENT_LENGTH:
            content = content[:self.config.MAX_CONTENT_LENGTH]
        
        return {
            'content': content,
            'section_id': section_id,
            'document_path': document_path,
            'word_count': len(content.split()),
            'keywords': self.text_processor.extract_keywords(content, 5),
            'processing_timestamp': time.time()
        }

class LightweightRelevanceScorer:
    """Lightweight relevance scoring without heavy ML models."""
    
    def __init__(self, config: LightweightConfig):
        self.config = config
        self.text_processor = LightweightTextProcessor(config)
    
    def score_sections_fast(self, sections: List[Dict[str, Any]], 
                           persona: Dict[str, Any], 
                           job_description: str) -> List[Dict[str, Any]]:
        """Fast relevance scoring using simple algorithms."""
        
        # Extract persona keywords
        persona_keywords = self._extract_persona_keywords(persona)
        job_keywords = self.text_processor.extract_keywords(job_description, 10)
        
        all_keywords = set(persona_keywords + job_keywords)
        
        # Score each section
        for section in sections:
            section['score'] = self._calculate_simple_score(
                section['content'], all_keywords, persona, job_description
            )
        
        return sections
    
    def _extract_persona_keywords(self, persona: Dict[str, Any]) -> List[str]:
        """Extract keywords from persona description."""
        keywords = []
        
        # Add role-based keywords
        role = persona.get('role', '').lower()
        if 'travel' in role or 'planner' in role:
            keywords.extend(['travel', 'trip', 'tourism', 'vacation', 'hotel', 'restaurant'])
        elif 'student' in role:
            keywords.extend(['study', 'learn', 'education', 'exam', 'course'])
        elif 'analyst' in role or 'financial' in role:
            keywords.extend(['analysis', 'data', 'report', 'financial', 'business'])
        elif 'journalist' in role or 'reporter' in role:
            keywords.extend(['news', 'story', 'article', 'report', 'investigation'])
        elif 'legal' in role or 'lawyer' in role:
            keywords.extend(['legal', 'law', 'contract', 'compliance', 'regulation'])
        
        # Add explicit keywords if provided
        if 'keywords' in persona:
            keywords.extend(persona['keywords'])
        
        return list(set(keywords))
    
    def _calculate_simple_score(self, content: str, keywords: set, 
                               persona: Dict[str, Any], job_description: str) -> float:
        """Calculate simple relevance score."""
        
        content_lower = content.lower()
        
        # Keyword matching score
        keyword_matches = sum(1 for keyword in keywords if keyword.lower() in content_lower)
        keyword_score = keyword_matches / max(len(keywords), 1)
        
        # Content similarity to job description
        similarity_score = self.text_processor.simple_similarity(content, job_description)
        
        # Content length bonus (longer content may be more comprehensive)
        length_score = min(len(content.split()) / 100, 1.0)
        
        # Combine scores
        total_score = (
            keyword_score * 0.5 +
            similarity_score * 0.3 +
            length_score * 0.2
        )
        
        return min(total_score, 1.0)

class LightweightDocumentAnalyst:
    """Main lightweight analyst class optimized for performance constraints."""
    
    def __init__(self):
        self.config = LightweightConfig()
        self.config.validate_system_requirements()
        
        self.document_processor = LightweightDocumentProcessor(self.config)
        self.relevance_scorer = OptimizedRelevanceScorer()  # Use optimized scorer for challenge criteria
        
        print("🚀 Lightweight Document Analyst initialized")
        print(f"   • CPU-only mode: {self.config.CPU_ONLY}")
        print(f"   • No internet access: {self.config.NO_INTERNET}")
        print(f"   • Max processing time: {self.config.MAX_PROCESSING_TIME_SECONDS}s")
        print(f"   • Max memory usage: {self.config.MAX_MEMORY_USAGE_GB}GB")
    
    def analyze_documents_fast(self, document_paths: List[str], 
                              persona: Dict[str, Any], 
                              job_to_be_done: str, 
                              top_k: int = 10) -> Dict[str, Any]:
        """Fast document analysis with performance monitoring."""
        
        start_time = time.time()
        self.document_processor.start_processing_timer()
        
        print(f"\n📊 Starting analysis of {len(document_paths)} documents...")
        
        # Monitor memory usage
        initial_memory = psutil.Process().memory_info().rss / (1024**3)
        
        try:
            # Process documents
            all_sections = []
            for i, doc_path in enumerate(document_paths, 1):
                print(f"   Processing document {i}/{len(document_paths)}: {os.path.basename(doc_path)}")
                
                sections = self.document_processor.process_document_fast(doc_path)
                all_sections.extend(sections)
                
                # Check memory usage
                current_memory = psutil.Process().memory_info().rss / (1024**3)
                if current_memory > self.config.MAX_MEMORY_USAGE_GB:
                    print(f"⚠️  Memory usage high: {current_memory:.2f}GB")
            
            print(f"   Extracted {len(all_sections)} sections total")
            
            # Score sections using optimized relevance scorer
            print("   Calculating enhanced relevance scores...")
            
            # Combine all sections into one document for analysis
            combined_content = '\n'.join([section['content'] for section in all_sections])
            
            # Get enhanced relevance analysis
            relevance_analysis = self.relevance_scorer.calculate_enhanced_relevance_score(
                combined_content, persona, {'description': job_to_be_done}
            )
            
            # Create scored sections from the analysis
            top_sections = []
            section_scores = relevance_analysis.get('section_scores', [])
            subsection_scores = relevance_analysis.get('subsection_scores', [])
            
            # Combine section and subsection scores for final ranking
            for i, section_score in enumerate(section_scores[:top_k]):
                top_sections.append({
                    'content': section_score['content'],
                    'score': section_score['relevance_score'],
                    'rank': section_score['rank'],
                    'source': f"Section {i+1}",
                    'analysis_type': 'section',
                    'scoring_details': {
                        'keyword_match': section_score.get('keyword_match', 0),
                        'context_relevance': section_score.get('context_relevance', 0),
                        'content_quality': section_score.get('content_quality', 0)
                    }
                })
            
            # Add top subsections if we need more content
            remaining_slots = top_k - len(top_sections)
            for i, subsection_score in enumerate(subsection_scores[:remaining_slots]):
                top_sections.append({
                    'content': subsection_score['content'],
                    'score': subsection_score['relevance_score'],
                    'rank': subsection_score['rank'],
                    'source': f"{subsection_score['parent_section']} - {subsection_score['title']}",
                    'analysis_type': 'subsection',
                    'scoring_details': {
                        'keyword_density': subsection_score.get('keyword_density', 0),
                        'specificity_score': subsection_score.get('specificity_score', 0),
                        'actionability_score': subsection_score.get('actionability_score', 0)
                    }
                })
            
            # Calculate performance metrics
            end_time = time.time()
            processing_time = end_time - start_time
            final_memory = psutil.Process().memory_info().rss / (1024**3)
            memory_used = final_memory - initial_memory
            
            print(f"\n✅ Analysis completed in {processing_time:.2f}s")
            print(f"   Memory used: {memory_used:.3f}GB")
            print(f"   Top relevance score: {top_sections[0]['score']:.3f}" if top_sections else "No results")
            
            # Create results with performance metrics
            results = {
                'analysis_results': top_sections,
                'performance_metrics': {
                    'processing_time_seconds': processing_time,
                    'memory_used_gb': memory_used,
                    'documents_processed': len(document_paths),
                    'sections_analyzed': len(all_sections),
                    'cpu_only': self.config.CPU_ONLY,
                    'internet_access': not self.config.NO_INTERNET,
                    'within_time_limit': processing_time <= self.config.MAX_PROCESSING_TIME_SECONDS,
                    'within_memory_limit': memory_used <= self.config.MAX_MEMORY_USAGE_GB
                },
                'metadata': {
                    'persona': persona,
                    'job_to_be_done': job_to_be_done,
                    'timestamp': time.time(),
                    'config': {
                        'max_processing_time': self.config.MAX_PROCESSING_TIME_SECONDS,
                        'max_memory_usage': self.config.MAX_MEMORY_USAGE_GB,
                        'cpu_only': self.config.CPU_ONLY
                    }
                }
            }
            
            return results
            
        except TimeoutError as e:
            print(f"❌ {e}")
            raise
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            raise

def run_lightweight_demo():
    """Demonstrate the lightweight system with performance constraints."""
    
    print("🎯 LIGHTWEIGHT CPU-ONLY DOCUMENT ANALYST DEMO")
    print("=" * 60)
    print("Performance Constraints:")
    print("• CPU-only processing")
    print("• Model size ≤ 1GB")
    print("• Processing time ≤ 60 seconds")
    print("• No internet access")
    print("=" * 60)
    
    # Initialize lightweight analyst
    analyst = LightweightDocumentAnalyst()
    
    # Test with Collection 1 (travel documents)
    collection_path = "Collection 1/PDFs"
    documents = [
        f"{collection_path}/South of France - Cities.pdf",
        f"{collection_path}/South of France - Cuisine.pdf", 
        f"{collection_path}/South of France - Restaurants and Hotels.pdf",
        f"{collection_path}/South of France - Things to Do.pdf"
    ]
    
    # Filter existing documents
    existing_docs = [doc for doc in documents if os.path.exists(doc)]
    
    if not existing_docs:
        print("❌ No documents found. Please ensure PDFs are in Collection 1/PDFs/")
        return
    
    persona = {
        'role': 'Travel Planner',
        'experience_level': 'Professional',
        'domain': 'Tourism',
        'keywords': ['travel', 'tourism', 'hotels', 'restaurants', 'attractions']
    }
    
    job = "Plan a 4-day cultural and culinary tour of South of France for 10 college friends"
    
    try:
        # Run analysis
        results = analyst.analyze_documents_fast(
            document_paths=existing_docs,
            persona=persona,
            job_to_be_done=job,
            top_k=5
        )
        
        # Display results
        print(f"\n📋 ANALYSIS RESULTS")
        print("-" * 40)
        
        performance = results['performance_metrics']
        print(f"✅ Performance Summary:")
        print(f"   • Processing Time: {performance['processing_time_seconds']:.2f}s (limit: 60s)")
        print(f"   • Memory Used: {performance['memory_used_gb']:.3f}GB (limit: 1GB)")
        print(f"   • Documents Processed: {performance['documents_processed']}")
        print(f"   • Sections Analyzed: {performance['sections_analyzed']}")
        print(f"   • CPU Only: {performance['cpu_only']}")
        print(f"   • Within Time Limit: {performance['within_time_limit']}")
        print(f"   • Within Memory Limit: {performance['within_memory_limit']}")
        
        print(f"\n📄 Top Relevant Sections:")
        for i, section in enumerate(results['analysis_results'][:3], 1):
            print(f"\n{i}. Score: {section['score']:.3f}")
            print(f"   Document: {os.path.basename(section['document_path'])}")
            print(f"   Content: {section['content'][:150]}...")
            print(f"   Keywords: {', '.join(section['keywords'])}")
        
        # Save results
        output_file = "lightweight_analysis_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

if __name__ == "__main__":
    run_lightweight_demo()
