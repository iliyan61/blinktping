# Use a lightweight Python image with GPIO support (for Raspberry Pi)
FROM arm32v6/python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev python3-dev

# Copy the code from your repository to the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install necessary system dependencies
RUN apk --update add --no-cache \
    bash \
    iputils

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Run the script
CMD ["python", "blinktping.py"]
