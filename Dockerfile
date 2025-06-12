# Stage 1: Base build stage
FROM python:3.13-slim AS builder

# Install system dependencies needed to build psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Upgrade pip and install dependencies
RUN pip install --upgrade pip 
COPY requirements.txt /app/ 
RUN pip install --no-cache-dir -r requirements.txt
 
# Stage 2: Production stage
FROM python:3.13-slim

# Install runtime dependencies only if needed (e.g., libpq5 for psycopg2 binary compatibility)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user and app directories
RUN useradd -m -r appuser && \
    mkdir -p /app && \
    mkdir -p /var/www/html/staticfiles && \
    mkdir -p /var/www/html/mediafiles && \
    chown -R appuser /app && \
    chown -R appuser /var/www/html

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy application code with ownership
COPY --chown=appuser:appuser . .

# Optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000 

# Make entrypoint executable
RUN chmod +x /app/entrypoint.prod.sh

# Start app
CMD ["/app/entrypoint.prod.sh"]