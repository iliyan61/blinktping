# Use a lightweight Python image with GPIO support (for Raspberry Pi)
FROM arm32v6/python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the code from your repository to the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Grant access to the GPIO and network utilities
RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Run the script
CMD ["python", "blinktping.py"]