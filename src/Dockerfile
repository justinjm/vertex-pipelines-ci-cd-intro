FROM python:3.7-slim AS builder
COPY requirements.txt .

# Install required Python packages 
RUN pip install -r requirements.txt

# Copy downloaded dependencies
COPY . .
