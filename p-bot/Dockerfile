# Use official Python image
FROM python:3.10-slim

WORKDIR /app

# Copy backend code
COPY backend/ .

# Copy framework code
COPY ../framework/agno/libs/agno /app/framework/agno/libs/agno
COPY ../framework/adk-python /app/framework/adk-python

# Set PYTHONPATH so Python can find the framework modules
ENV PYTHONPATH="/app/framework/agno/libs/agno:/app/framework/adk-python:${PYTHONPATH}"

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"] 