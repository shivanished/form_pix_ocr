FROM python:3.11-slim

# Install ImageMagick and Tesseract
RUN apt-get update && apt-get install -y \
    imagemagick \
    libmagickwand-dev \
    tesseract-ocr \
    libtesseract-dev

# Set up environment variables
ENV MAGICK_HOME="/usr"
ENV LD_LIBRARY_PATH="$MAGICK_HOME/lib:$LD_LIBRARY_PATH"
ENV PATH="/usr/bin:$MAGICK_HOME/bin:$PATH"
ENV TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata"

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

COPY . .

CMD ["/opt/venv/bin/hypercorn", "main:app", "--bind", "0.0.0.0:8000"]