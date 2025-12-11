# Use official Python runtime
from python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Run migrations and start server
# Note: In production, it's often better to run migrations in a separate step, 
# but for this "All-in-One" deploy, we'll do it on boot.
CMD python manage.py migrate && python manage.py ensure_admin && gunicorn journal_core.wsgi:application --bind 0.0.0.0:$PORT
