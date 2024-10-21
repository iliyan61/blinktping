# Use a lightweight Python image with GPIO support (for Raspberry Pi)
FROM arm32v6/python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the code from your repository to the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install necessary system dependencies
RUN apk add --no-cache \
    bash \
    iputils

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1
ENV DISCORD_WEBHOOK_URL='your_webhook_url_here'

# Run the script
CMD ["python", "blinktping.py"]