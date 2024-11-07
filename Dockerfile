# Stage 1: Build stage
FROM python:3.12-slim AS builder

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Stage 2: Final stage
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the dependencies from the build stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app

# Expose the port
EXPOSE 8000

# Set the SSL_CERT_FILE environment variable
RUN SSL_CERT_FILE=$(python3 -m certifi)
ENV SSL_CERT_FILE=$SSL_CERT_FILE

# Run the application
CMD ["python3", "main.py"]