FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
pip install uvicorn fastapi

# Copy the current directory contents into the container
COPY . /app

# Command to run on container start
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]