FROM python:3.11-slim

# Install ImageMagick
RUN apt-get update && apt-get install -y \
    imagemagick \
    libmagickwand-dev

# Set up environment variables for ImageMagick
ENV MAGICK_HOME="/usr"
ENV LD_LIBRARY_PATH="$MAGICK_HOME/lib:$LD_LIBRARY_PATH"
ENV PATH="$MAGICK_HOME/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Hypercorn separately to ensure it's available
RUN pip install hypercorn

# Copy the application code
COPY . .

# Command to run your FastAPI application
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000"]
