# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Environment Variables ----------
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# ---------- System Dependencies ----------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# ---------- Upgrade pip, setuptools, wheel ----------
RUN pip install --upgrade pip setuptools wheel

# ---------- Copy App ----------
WORKDIR /app
COPY . /app

# ---------- Install Python Dependencies ----------
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# ---------- Create Output Directory ----------
RUN mkdir -p /app/static/output

# ---------- Expose Port ----------
EXPOSE 3000

# ---------- Run Flask App ----------
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:3000", "--workers", "1"]
