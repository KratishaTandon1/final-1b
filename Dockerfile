# Lightweight single-stage build for CPU-only deployment
FROM python:3.11-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash analyst

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies as root
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Copy application code and set ownership
COPY . /app
RUN chown -R analyst:analyst /app

# Switch to non-root user
USER analyst

# Set Python environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Scoring optimization environment variables
ENV SCORING_OPTIMIZED=true
ENV SECTION_RELEVANCE_WEIGHT=60
ENV SUBSECTION_RELEVANCE_WEIGHT=40

# Default command
CMD ["python", "challenge_lightweight_processor.py"]