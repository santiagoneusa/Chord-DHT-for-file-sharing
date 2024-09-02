FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN cp /app/src/peer/.env.example /app/src/peer/.env
RUN cp /app/src/server/.env.example /app/src/server/.env

EXPOSE 6000
