# Best base for 2026: slim, secure, Python 3.12 (or change to your version)
FROM python:3.12-slim-bookworm

# Good defaults for Docker + Django
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Working dir inside container
WORKDIR /app

# Install OS-level deps (for psycopg2 if using Postgres, etc.)
RUN apt-get update --no-install-recommends && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first → better caching on rebuilds
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy full project code
COPY . .

# Collect static during build (fast, cached; fails gracefully if no static)
RUN python manage.py collectstatic --noinput --clear || true

# Render assigns $PORT dynamically (usually 10000)
EXPOSE ${PORT:-10000}

# At container start: migrate → start server
# Replace 'andy' below with your ACTUAL Django project name!
#   → look inside the folder containing settings.py / wsgi.py (probably 'andy' or 'ANDY')
CMD ["sh", "-c", "python manage.py migrate && gunicorn andy.wsgi:application --bind 0.0.0.0:${PORT:-10000} --workers 3 --timeout 30"]