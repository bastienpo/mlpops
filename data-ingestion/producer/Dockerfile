FROM python:3.11.7-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "milvus_ingestion.py"]
