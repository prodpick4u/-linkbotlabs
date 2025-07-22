# Dockerfile

FROM python:3.12-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
 && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project files into container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Default command (can be overridden in workflow)
CMD ["python", "video_creator_save_only.py"]
