# Dockerfile for TestFlow AI - Black-Box E2E Testing SaaS
# Base image with Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # For Chrome/Chromium (needed for Selenium)
    wget \
    gnupg \
    ca-certificates \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (for Selenium WebDriver)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Create directory for test reports
RUN mkdir -p reports screenshots

# Expose port (for future web UI)
EXPOSE 8000

# Default command: run Behave tests
CMD ["behave", "acceptance_tests/", "--no-capture"]
