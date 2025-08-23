# Use a stable Python version compatible with MoviePy and NumPy
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Clear pip cache
RUN pip cache purge

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 3000

# Run the app with Gunicorn
CMD ["gunicorn", "-k", "gthread", "-w", "2", "-b", "0.0.0.0:3000", "app:app"]
