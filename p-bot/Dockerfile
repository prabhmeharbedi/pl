# Use official Python image
FROM python:3.10-slim

WORKDIR /app

# Copy backend code (including framework files that are already in backend/framework)
COPY backend/ .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH so Python can find the framework modules
ENV PYTHONPATH="/app/framework:/app/framework/agno:/app/framework/adk-python:${PYTHONPATH}"

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"] 