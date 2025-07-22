FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run script
CMD ["python", "video_creator_save_only.py"]
