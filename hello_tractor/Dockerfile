# Use Python 3.10 with Debian Bullseye base image
FROM python:3.10-bullseye

# Set working directory inside the container
WORKDIR /usr/app/

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Create a virtual environment, upgrade pip, and install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Set the virtual environment PATH for all subsequent commands
ENV PATH="/opt/venv/bin:$PATH"

# Copy the rest of the application code into the container
COPY . .

# Create a directory for static files
RUN mkdir -p /usr/app/staticfiles

# Expose the application port
EXPOSE 8000

# Copy and make the entrypoint script executable
COPY entrypoint.sh /usr/app/
RUN chmod +x /usr/app/entrypoint.sh

# Use the entrypoint script to start the application
ENTRYPOINT ["/usr/app/entrypoint.sh"]
