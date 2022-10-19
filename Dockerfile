# Download dependencies to /root/.local.
FROM python:3.7-slim AS builder
COPY requirements.txt .

RUN pip install -r requirements.txt

# # Pull new image to only keep the things we need.
# FROM python:3.7-slim
# WORKDIR /src

# Copy downloaded dependencies.
# COPY --from=builder /root/.local /root/.local
COPY . .

# Update python path.
# ENV PATH=/root/.local:$PATH
