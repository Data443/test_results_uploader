# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files to the container
COPY main.py /app/
COPY requirements.txt /app/
COPY entrypoint.sh /app/  

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set executable permissions for main.py and entrypoint.sh
RUN chmod +x /app/main.py
RUN chmod +x /app/entrypoint.sh

# Update the entrypoint to accept arguments
ENTRYPOINT ["./entrypoint.sh"]