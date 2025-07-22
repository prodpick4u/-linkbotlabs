# Use a base image with Python and system tools
FROM python:3.12-slim

# Install ffmpeg and imagemagick
RUN apt-get update && \
    apt-get install -y ffmpeg imagemagick libx11-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the repo
COPY . .

# Run your script
CMD ["python", "video_creator_save_only.py"]
