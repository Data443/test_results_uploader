# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files to the container
COPY entrypoint.sh /app
COPY main.py /app
COPY requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the entrypoint for the container
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
