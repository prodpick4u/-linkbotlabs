# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all code
COPY . .

# Expose port
EXPOSE 3000

# Run Flask app with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:3000"]
