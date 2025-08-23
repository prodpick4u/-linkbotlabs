# Use a stable Python version compatible with MoviePy and NumPy
FROM python:3.10-slim

# Install system dependencies needed by MoviePy and ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port for Flask (optional)
EXPOSE 3000

# Run your main app by default
CMD ["python", "app.py"]
