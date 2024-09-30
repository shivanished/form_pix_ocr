FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    imagemagick \
    libmagickwand-dev \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up environment variables
ENV MAGICK_HOME="/usr"
ENV LD_LIBRARY_PATH="$MAGICK_HOME/lib:$LD_LIBRARY_PATH"
ENV PATH="/usr/bin:$MAGICK_HOME/bin:$PATH"
ENV TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata"

WORKDIR /app

# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir hypercorn

# Verify installations
RUN which hypercorn || echo "Hypercorn not found in PATH"
RUN which tesseract
RUN tesseract --version

# Copy the application code
COPY . .

# Update the Tesseract path in the Python code
RUN sed -i 's|r'/opt/homebrew/bin/tesseract'|r'/usr/bin/tesseract'|g' main.py

# Command to run your FastAPI application
CMD ["python", "-m", "hypercorn", "main:app", "--bind", "0.0.0.0:8000"]