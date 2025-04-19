FROM python:3.12
WORKDIR /app
# Copy requirements files first to leverage Docker cache
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copy source code
COPY backend/ .
# Expose the port the app runs on
EXPOSE 8001
# Run the application
CMD ["python", "main.py"]
# Use the following command to build the Docker image (from parent directory!)
# docker build -t backend:latest .
# Use the following command to run the Docker container 
# docker run -d -p 8001:8001 backend:latest
# Use the following command to run the Docker container with a volume
# docker run -d -p 8001:8001 -v $(pwd):/app backend:latest