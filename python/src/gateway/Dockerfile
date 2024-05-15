FROM python:3.10-slim-bullseye

RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirement.txt /app
RUN pip install --no-cache-dir --requirement /app/requirement.txt
COPY . /app

EXPOSE 8080

CMD ["python3", "server.py"]

