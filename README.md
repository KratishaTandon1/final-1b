# Intelligent Document Analyst

An intelligent document analysis system that extracts and prioritizes the most relevant sections from a collection of documents based on a specific persona and their job-to-be-done.

## Features

- **Multi-format Document Support**: Supports PDF, DOCX, and TXT files
- **Persona-Based Analysis**: Tailors document analysis to specific user personas
- **Job-to-be-Done Framework**: Prioritizes content based on specific tasks or goals
- **Intelligent Scoring**: Uses NLP and machine learning to score document relevance
- **Section Extraction**: Identifies and extracts the most relevant document sections
- **Prioritized Output**: Presents results ranked by relevance score

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

### Basic Usage

```python
from document_analyst import DocumentAnalyst

# Initialize the analyst
analyst = DocumentAnalyst()

# Define persona and job-to-be-done
persona = {
    "role": "Data Scientist",
    "experience_level": "Senior",
    "domain": "Healthcare",
    "goals": ["machine learning", "data analysis", "statistical modeling"]
}

job_to_be_done = "Find best practices for implementing machine learning models in healthcare data analysis"

# Analyze documents
results = analyst.analyze_documents(
    document_paths=["doc1.pdf", "doc2.docx", "doc3.txt"],
    persona=persona,
    job_to_be_done=job_to_be_done,
    top_k=5
)

# Display results
for result in results:
    print(f"Document: {result['document']}")
    print(f"Section: {result['section']}")
    print(f"Relevance Score: {result['score']:.3f}")
    print(f"Content: {result['content'][:200]}...")
    print("-" * 50)
```

### Command Line Interface

```bash
python main.py analyze --documents "docs/*.pdf" --persona-file persona.json --job "Find ML best practices" --output results.json
```

### Docker Usage

1. Build the Docker image:
```bash
docker build -t document-analyst-demo .
```

2. Run the Docker container with volume mounts for collections:
```bash
# Windows PowerShell
docker run --rm -it -v "${PWD}:/app" document-analyst-demo

# Linux/macOS
docker run --rm -it -v "$(pwd):/app" document-analyst-demo
```

The program will:
- Process all collections in the mounted folders
- Generate `challenge1b_output.json` in each Collection folder
- Display processing summary and performance metrics

## Project Structure

```
document_analyst/
├── document_analyst/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   ├── persona_analyzer.py
│   │   └── relevance_scorer.py
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py
│   │   ├── docx_parser.py
│   │   └── txt_parser.py
│   └── utils/
│       ├── __init__.py
│       └── text_processing.py
├── examples/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## Configuration

The system can be configured through environment variables or configuration files. See `config.py` for available options.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request
