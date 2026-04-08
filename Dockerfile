FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; else \
    pip install --no-cache-dir \
    requests \
    python-dotenv \
    google-analytics-data \
    google-api-python-client \
    google-auth \
    beautifulsoup4 \
    numpy \
    scikit-learn \
    textstat; fi

# Copy project files
COPY . .

# Default command runs the research scripts
CMD ["python3", "research_trending.py"]
