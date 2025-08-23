# ----------------------------
# Use stable Python 3.11
# ----------------------------
FROM python:3.11-slim

# ----------------------------
# Install system dependencies
# ----------------------------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Set working directory
# ----------------------------
WORKDIR /app

# ----------------------------
# Copy project files
# ----------------------------
COPY . /app

# ----------------------------
# Upgrade pip and install Python dependencies
# ----------------------------
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ----------------------------
# Expose Flask port
# ----------------------------
EXPOSE 3000

# ----------------------------
# Default command: use Gunicorn
# ----------------------------
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:3000", "--workers", "2"]
