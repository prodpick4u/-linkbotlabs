# ----------------------------
# Base Image
# ----------------------------
FROM python:3.10-slim

# ----------------------------
# Environment Variables
# ----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# ----------------------------
# System Dependencies
# ----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Set Working Directory
# ----------------------------
WORKDIR /app

# ----------------------------
# Copy Requirements
# ----------------------------
COPY requirements.txt .

# ----------------------------
# Install Python Dependencies
# ----------------------------
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ----------------------------
# Copy Application Code
# ----------------------------
COPY . .

# ----------------------------
# Expose Port
# ----------------------------
EXPOSE 3000

# ----------------------------
# Start Command
# ----------------------------
CMD ["gunicorn", "-k", "gthread", "-w", "2", "-b", "0.0.0.0:3000", "app:app"]
