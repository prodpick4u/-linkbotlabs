# -------------------------------
# Base image with Python 3.10
# -------------------------------
FROM python:3.10-slim

# -------------------------------
# Set working directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Install system dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
    build-essential \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Copy project files
# -------------------------------
COPY . /app

# -------------------------------
# Upgrade pip and install Python packages
# -------------------------------
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Expose port and start server
# -------------------------------
EXPOSE 3000
CMD ["gunicorn", "-k", "gthread", "-w", "2", "-b", "0.0.0.0:3000", "app:app"]
