# Use a stable Python version compatible with MoviePy & NumPy
FROM python:3.11-slim

# Install system dependencies needed by MoviePy & ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip & install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 3000

# Default command for Render
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:3000", "--workers", "2"]
