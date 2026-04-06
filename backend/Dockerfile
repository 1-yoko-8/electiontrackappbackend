FROM python:3.11-slim

# Set working directory
WORKDIR /backend

# Ensure Python knows where to find packages
ENV PYTHONPATH=/backend

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the rest of the project
COPY . .

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]