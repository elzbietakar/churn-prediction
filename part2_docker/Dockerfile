FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/part2_docker

ENV PYTHONPATH=/app
ENV FLASK_APP=part2_docker.api

EXPOSE 5000 8501

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
