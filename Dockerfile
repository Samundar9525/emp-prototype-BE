# Backend Dockerfile
FROM python:3.12-slim

# Set env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=emp_management.settings

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create staticfiles directory and set permissions
RUN mkdir -p /app/staticfiles && chmod 755 /app/staticfiles

# Create non-root user
RUN adduser --disabled-password --gecos '' django && chown -R django:django /app
USER django

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Expose port
EXPOSE 8000

# Run with Gunicorn
CMD ["gunicorn", "emp_management.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
