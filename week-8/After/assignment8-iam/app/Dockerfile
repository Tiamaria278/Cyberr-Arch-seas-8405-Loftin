FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]