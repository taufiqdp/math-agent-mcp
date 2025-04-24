# Build stage
FROM python:3.13-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt


# Final stage
FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /root/.local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

CMD ["python"]

