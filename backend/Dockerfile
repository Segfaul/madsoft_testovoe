# Backend Dockerfile

FROM python:3.11.6-slim

RUN mkdir -p /madsoft_testovoe/backend
WORKDIR /madsoft_testovoe

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
COPY backend ./backend
