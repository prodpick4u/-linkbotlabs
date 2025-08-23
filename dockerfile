# Use official Python base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for ffmpeg, Playwright, GTK, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    curl \
    wget \
    git \
    libglib2.0-0 \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Upgrade pip and install Python dependencies without cache
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 3000

# Start the app with Gunicorn
CMD ["gunicorn", "-k", "gthread", "-w", "2", "-b", "0.0.0.0:3000", "app:app"]
