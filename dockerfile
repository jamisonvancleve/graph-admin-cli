# 1. Base Image
FROM python:3.12-slim

# 2. Environment Configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Set Working Directory
WORKDIR /app

# 4. Dependency Layering (Optimized for Caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Application Code Copy
COPY main.py /app/main.py
COPY app/ /app/app/

# 6. Non-Root User Hardening & Directory Setup
RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -s /bin/sh appuser && \
    mkdir -p /app/logs && \
    chown -R appuser:appuser /app

# 7. Security Context Switch
USER appuser

# 8. Container Entrypoint
ENTRYPOINT ["python", "main.py"]