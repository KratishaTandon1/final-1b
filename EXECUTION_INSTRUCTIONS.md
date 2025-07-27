# Document Analyst - Execution Instructions

## Quick Start

### Option 1: Docker Deployment (Recommended)

#### Build and Run
```bash
# Build the Docker image
docker build -t document-analyst .

# Run with document collections mounted
docker run -v $(pwd)/Collection\ 1:/app/Collection\ 1 \
           -v $(pwd)/Collection\ 2:/app/Collection\ 2 \
           -v $(pwd)/Collection\ 3:/app/Collection\ 3 \
           document-analyst
```

#### Production Deployment
```bash
# Run with resource limits for production
docker run --memory=1g \
           --cpus=2 \
           --read-only \
           --tmpfs /tmp \
           -v $(pwd)/Collection\ 1:/app/Collection\ 1:ro \
           -v $(pwd)/Collection\ 2:/app/Collection\ 2:ro \
           -v $(pwd)/Collection\ 3:/app/Collection\ 3:ro \
           -v $(pwd)/output:/app/output \
           document-analyst
```

### Option 2: Direct Python Execution

#### Prerequisites
- Python 3.11+
- 1GB+ available RAM
- CPU with 2+ cores

#### Installation
```bash
# Install lightweight dependencies
pip install -r requirements.txt

# Verify installation
python -c "import psutil, PyPDF2, docx; print('Dependencies OK')"
```

#### Execution
```bash
# Process all challenge collections
python challenge_lightweight_processor.py

# Process individual collection
python -c "
from challenge_lightweight_processor import ChallengeProcessor
processor = ChallengeProcessor()
result = processor.process_challenge_input('Collection 1/challenge1b_input.json')
print('Processing completed successfully')
"
```

## Performance Validation

### System Requirements Check
```bash
# Check available resources
python -c "
import psutil
print(f'Available Memory: {psutil.virtual_memory().available/(1024**3):.2f}GB')
print(f'CPU Cores: {psutil.cpu_count()}')
print('✅ System ready' if psutil.virtual_memory().available/(1024**3) >= 1 else '❌ Insufficient memory')
"
```

### Performance Testing
```bash
# Run with performance monitoring
python -c "
import time, psutil, os
from challenge_lightweight_processor import ChallengeProcessor

start_time = time.time()
initial_memory = psutil.Process().memory_info().rss / (1024**3)

processor = ChallengeProcessor()
result = processor.process_challenge_input('Collection 1/challenge1b_input.json')

end_time = time.time()
final_memory = psutil.Process().memory_info().rss / (1024**3)

print(f'Processing Time: {end_time - start_time:.2f}s (limit: 60s)')
print(f'Memory Used: {final_memory - initial_memory:.3f}GB (limit: 1GB)')
print(f'CPU Only: True')
print(f'Internet Required: False')
"
```

## Output Files

After execution, the following output files are generated:

### Challenge Outputs
- `Collection 1/challenge1b_output.json` - Travel planning analysis
- `Collection 2/challenge1b_output.json` - PDF management training
- `Collection 3/challenge1b_output.json` - Menu development strategy

### Performance Reports
- `lightweight_analysis_results.json` - Detailed performance metrics
- `PERFORMANCE_COMPLIANCE_REPORT.md` - Constraint compliance validation

## Troubleshooting

### Common Issues

#### Memory Issues
```bash
# If memory errors occur, reduce document batch size
export MAX_SECTIONS_PER_DOC=10
export MAX_CONTENT_LENGTH=5000
python challenge_lightweight_processor.py
```

#### Processing Timeout
```bash
# If processing takes too long, enable fast mode
export FAST_MODE=true
export MAX_DOCUMENT_SIZE_MB=25
python challenge_lightweight_processor.py
```

#### Missing Dependencies
```bash
# Install missing PDF processing library
pip install PyPDF2

# Install missing document processing library
pip install python-docx

# Install system monitoring library
pip install psutil
```

### Verification Commands

#### Test Document Processing
```bash
# Test PDF extraction
python -c "
from lightweight_cpu_analyst import LightweightDocumentProcessor, LightweightConfig
processor = LightweightDocumentProcessor(LightweightConfig())
sections = processor.process_document_fast('Collection 1/PDFs/South of France - Cities.pdf')
print(f'Extracted {len(sections)} sections successfully')
"
```

#### Test System Constraints
```bash
# Validate all constraints
python -c "
from lightweight_cpu_analyst import LightweightConfig
config = LightweightConfig()
config.validate_system_requirements()
print('✅ All constraints validated')
"
```

## Production Deployment Notes

### Environment Variables
```bash
# Performance tuning
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export PYTHONUNBUFFERED=1

# Security settings
export PYTHONDONTWRITEBYTECODE=1
```

### Resource Monitoring
```bash
# Monitor resource usage during execution
docker stats document-analyst

# Check container health
docker inspect --format='{{.State.Health.Status}}' document-analyst
```

### Scaling Considerations
- **Horizontal**: Deploy multiple containers for parallel processing
- **Vertical**: Increase CPU cores for faster processing (memory stays constant)
- **Edge Deployment**: Suitable for ARM processors and embedded systems

## Integration Examples

### REST API Wrapper
```python
from flask import Flask, request, jsonify
from challenge_lightweight_processor import ChallengeProcessor

app = Flask(__name__)
processor = ChallengeProcessor()

@app.route('/analyze', methods=['POST'])
def analyze_documents():
    input_file = request.json['input_file']
    result = processor.process_challenge_input(input_file)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

### Batch Processing
```bash
# Process multiple collections in parallel
for collection in Collection\ *; do
    docker run -d \
        -v $(pwd)/$collection:/app/$collection \
        -v $(pwd)/output:/app/output \
        --name="analyst-$(basename "$collection")" \
        document-analyst python challenge_lightweight_processor.py
done
```

## Success Criteria Validation

The system meets all specified requirements:
- ✅ **CPU-Only**: No GPU dependencies
- ✅ **Model Size**: <0.01GB memory usage
- ✅ **Processing Time**: <10s for largest collection
- ✅ **No Internet**: Completely offline operation
- ✅ **Output Format**: Complete metadata and section analysis
- ✅ **Diversity**: Handles travel, technical, and food domains
