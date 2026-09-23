FROM python:3.12-slim

WORKDIR /app
COPY nebius_nighteye/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY nebius_nighteye /app/nebius_nighteye

ENV PORT=8080
CMD ["sh", "-c", "uvicorn nebius_nighteye.app:app --host 0.0.0.0 --port ${PORT}"]
