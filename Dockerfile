# Dockerfile — tells Hugging Face how to run our app
# ====================================================
 
# Start from Python 3.10 base image
FROM python:3.10-slim
 
# Set working directory inside container
WORKDIR /app
 
# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*
 
# Copy requirements first (for faster rebuilds)
COPY requirements.txt .
 
# Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy all project files
COPY . .
 
# Create uploads folder
RUN mkdir -p static/uploads
 
# Hugging Face Spaces uses port 7860
EXPOSE 7860
 
# Start the Flask app
CMD ["python", "app.py"]
