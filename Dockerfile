# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files to the container
COPY entrypoint.sh /app/
COPY main.py /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set executable permissions for entrypoint.sh
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/main.py
RUN chmod +x /app/requirements.txt


# Set the entrypoint for the container
ENTRYPOINT ["/app/entrypoint.sh"]
# FROM python:3.9-slim

# Set the working directory inside the container
# WORKDIR /app

# Copy the necessary files to the container
# COPY entrypoint.sh /app/
# COPY main.py /app/
# COPY requirements.txt /app/

# Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Set executable permissions for entrypoint.sh
# RUN chmod +x /app/entrypoint.sh

# Set the entrypoint for the container
# ENTRYPOINT ["/app/entrypoint.sh"]
# ENTRYPOINT ["python", "/app/main.py"] 