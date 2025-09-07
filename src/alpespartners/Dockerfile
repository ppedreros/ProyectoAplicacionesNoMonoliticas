FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app/
WORKDIR /app/alpespartners
RUN pip install -e ..

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
