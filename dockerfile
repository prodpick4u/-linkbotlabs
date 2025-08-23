# Use a slim Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for building packages and running ffmpeg / Playwright
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
    libpango1.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip separately
RUN python -m pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 3000

# Start the app using Gunicorn
CMD ["gunicorn", "-k", "gthread", "-w", "2", "-b", "0.0.0.0:3000", "app:app"]
