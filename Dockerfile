FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

# Install ImageMagick and Tesseract
RUN apt-get update && apt-get install -y \
    imagemagick \
    libmagickwand-dev \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng

# Set up environment variables
ENV MAGICK_HOME="/usr"
ENV LD_LIBRARY_PATH="$MAGICK_HOME/lib:$LD_LIBRARY_PATH"
ENV PATH="/usr/bin:$MAGICK_HOME/bin:$PATH"
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir hypercorn

# Verify installations
RUN which hypercorn || echo "Hypercorn not found in PATH"
RUN which tesseract
RUN ls -l /usr/bin/tesseract
RUN tesseract --version
RUN tesseract --list-langs
RUN ls -l $TESSDATA_PREFIX

COPY . .

# Update Tesseract path in main.py
RUN sed -i 's|r'/opt/homebrew/bin/tesseract'|'/usr/bin/tesseract'|g' main.py

CMD ["/opt/venv/bin/hypercorn", "main:app", "--bind", "0.0.0.0:8000"]