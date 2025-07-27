"""
Project structure summary and getting started guide.
"""

import os
from pathlib import Path

def print_project_structure():
    """Print the project structure."""
    
    print("INTELLIGENT DOCUMENT ANALYST - PROJECT STRUCTURE")
    print("=" * 60)
    
    root_dir = Path(__file__).parent
    
    def print_tree(directory, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
            
        items = sorted(directory.iterdir())
        dirs = [item for item in items if item.is_dir() and not item.name.startswith('.')]
        files = [item for item in items if item.is_file() and not item.name.startswith('.')]
        
        # Print directories first
        for i, item in enumerate(dirs):
            is_last = i == len(dirs) - 1 and len(files) == 0
            print(f"{prefix}{'└── ' if is_last else '├── '}{item.name}/")
            extension = "    " if is_last else "│   "
            print_tree(item, prefix + extension, max_depth, current_depth + 1)
        
        # Print files
        for i, item in enumerate(files):
            is_last = i == len(files) - 1
            print(f"{prefix}{'└── ' if is_last else '├── '}{item.name}")
    
    print_tree(root_dir)
    
    print("\n" + "=" * 60)
    print("KEY COMPONENTS:")
    print("=" * 60)
    
    components = [
        ("document_analyst/", "Main package containing the core functionality"),
        ("├── core/", "Core analysis components"),
        ("│   ├── document_processor.py", "Handles document parsing and processing"),
        ("│   ├── persona_analyzer.py", "Analyzes persona and job requirements"),
        ("│   └── relevance_scorer.py", "Scores document sections for relevance"),
        ("├── parsers/", "Document format parsers"),
        ("│   ├── pdf_parser.py", "PDF document parser"),
        ("│   ├── docx_parser.py", "Microsoft Word document parser"),
        ("│   └── txt_parser.py", "Plain text document parser"),
        ("└── utils/", "Utility functions"),
        ("    └── text_processing.py", "Text segmentation and preprocessing"),
        ("main.py", "Command-line interface"),
        ("demo.py", "Comprehensive demonstration script"),
        ("config.py", "Configuration management"),
        ("requirements.txt", "Python dependencies"),
        ("tests/", "Unit and integration tests"),
        ("examples/", "Usage examples"),
    ]
    
    for component, description in components:
        print(f"{component:<30} {description}")

def print_usage_examples():
    """Print usage examples."""
    
    print("\n" + "=" * 60)
    print("GETTING STARTED:")
    print("=" * 60)
    
    print("\n1. INSTALLATION:")
    print("-" * 30)
    print("pip install -r requirements.txt")
    print("python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')\"")
    
    print("\n2. RUN DEMONSTRATION:")
    print("-" * 30)
    print("python demo.py")
    print("# OR")
    print("python main.py demo")
    
    print("\n3. ANALYZE YOUR DOCUMENTS:")
    print("-" * 30)
    print("python main.py analyze \\")
    print("    --documents \"path/to/your/documents/*.pdf\" \\")
    print("    --role \"Data Scientist\" \\")
    print("    --experience \"Senior\" \\")
    print("    --domain \"Healthcare\" \\")
    print("    --goals \"machine learning,data analysis\" \\")
    print("    --job \"Find ML best practices\" \\")
    print("    --top-k 5")
    
    print("\n4. PROGRAMMATIC USAGE:")
    print("-" * 30)
    print("""
from document_analyst import DocumentAnalyst

# Initialize
analyst = DocumentAnalyst()

# Define persona
persona = {
    "role": "Data Scientist",
    "experience_level": "Senior", 
    "domain": "Healthcare",
    "goals": ["machine learning", "data analysis"]
}

# Analyze documents
results = analyst.analyze_documents(
    document_paths=["doc1.pdf", "doc2.txt"],
    persona=persona,
    job_to_be_done="Find ML best practices",
    top_k=5
)

# Process results
for result in results:
    print(f"Score: {result['score']:.3f}")
    print(f"Content: {result['content'][:100]}...")
    """)

def print_features():
    """Print system features."""
    
    print("\n" + "=" * 60)
    print("SYSTEM FEATURES:")
    print("=" * 60)
    
    features = [
        "✓ Multi-format document support (PDF, DOCX, TXT)",
        "✓ Persona-based content analysis",
        "✓ Job-to-be-done framework integration",
        "✓ Intelligent text segmentation",
        "✓ TF-IDF + keyword + semantic scoring",
        "✓ Configurable relevance weights",
        "✓ Command-line interface",
        "✓ Programmatic Python API",
        "✓ Comprehensive test suite",
        "✓ Extensible architecture",
    ]
    
    for feature in features:
        print(f"  {feature}")

def print_configuration():
    """Print configuration options."""
    
    print("\n" + "=" * 60)
    print("CONFIGURATION OPTIONS:")
    print("=" * 60)
    
    configs = [
        ("MIN_SECTION_LENGTH", "100", "Minimum section length for analysis"),
        ("MAX_SECTION_LENGTH", "2000", "Maximum section length"),
        ("TFIDF_WEIGHT", "0.4", "Weight for TF-IDF scoring"),
        ("KEYWORD_WEIGHT", "0.4", "Weight for keyword matching"),
        ("SEMANTIC_WEIGHT", "0.2", "Weight for semantic similarity"),
        ("DEFAULT_TOP_K", "10", "Default number of results to return"),
    ]
    
    print("Environment Variables:")
    print("-" * 30)
    for var, default, description in configs:
        print(f"{var:<20} = {default:<6} # {description}")

if __name__ == "__main__":
    print_project_structure()
    print_usage_examples()
    print_features()
    print_configuration()
    
    print("\n" + "=" * 60)
    print("Ready to analyze your documents! 🚀")
    print("=" * 60)
