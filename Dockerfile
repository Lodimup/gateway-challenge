FROM python:3.11-slim

WORKDIR /app

COPY app /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]