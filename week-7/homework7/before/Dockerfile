FROM python:3.11-alpine

RUN addgroup -S appgroup && adduser -S -G appgroup appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

CMD ["python", "app.py"]
