# Builder stage
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies only for compiling packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Preinstall wheel for better binary installs, and avoid pip cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Final runtime stage
FROM python:3.9-slim

WORKDIR /app

# Install only minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only what is needed from builder
COPY --from=builder /usr/local/lib/python3.9/ /usr/local/lib/python3.9/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Add non-root user
RUN useradd --create-home appuser

# Copy source code (only relevant files; ideally use .dockerignore to reduce context)
COPY . .

# Set permissions for non-root use
RUN chown -R appuser:appuser /app

USER appuser

# Environment configuration
ENV FLASK_APP=main.py 
ENV FLASK_RUN_PORT=5000 
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Entrypoint
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
