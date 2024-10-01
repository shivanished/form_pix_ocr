FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get install -y \
    imagemagick \
    libmagickwand-dev \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev

ENV MAGICK_HOME="/usr"
ENV LD_LIBRARY_PATH="$MAGICK_HOME/lib:$LD_LIBRARY_PATH"
ENV PATH="/usr/bin:$MAGICK_HOME/bin:$PATH"
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install hypercorn

RUN which python
RUN python --version
RUN echo $PATH
RUN which tesseract
RUN tesseract --version

COPY . .

CMD ["python", "-m", "hypercorn", "main:app", "--bind", "0.0.0.0:8000"]