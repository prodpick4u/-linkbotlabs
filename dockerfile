# Use a lightweight Python base image
FROM python:3.12-slim

# Install system dependencies needed by moviepy
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Optional: default command (can be overridden in GitHub Actions)
CMD ["python", "video_creator_save_only.py"]
