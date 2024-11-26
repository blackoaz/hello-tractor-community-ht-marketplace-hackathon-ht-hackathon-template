# Using Python 3.10 with Debian Bullseye base
FROM python:3.10-bullseye

# Setting working directory in the container
WORKDIR /usr/app/

# Copying requirements file first to leverage Docker caching
COPY requirements.txt .

# Creating virtual environment, upgrade pip, and install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Setting virtual environment PATH for all subsequent commands
ENV PATH="/opt/venv/bin:$PATH"

# Copying application code into the container
COPY . .

# Exposing the application port
EXPOSE 8000

# Copying the entrypoint script and make it executable
COPY entrypoint.sh /usr/app/
RUN chmod +x /usr/app/entrypoint.sh

# Using entrypoint script to run the application
CMD ["/usr/app/entrypoint.sh"]
