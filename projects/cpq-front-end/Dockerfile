FROM python:3.12-slim-bookworm

WORKDIR /app

# pymssql 2.3+ ships manylinux wheels for py3.12, so no freetds build deps needed.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py cost_drivers.json ./
COPY templates ./templates
COPY routes ./routes
COPY db ./db
COPY lib ./lib

EXPOSE 5050

# Default to prod-style server. The Makefile overrides this for `make run`.
CMD ["gunicorn", "-b", "0.0.0.0:5050", "--workers", "1", "--threads", "4", "--timeout", "120", "app:app"]
