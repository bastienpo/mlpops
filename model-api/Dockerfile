FROM python:3.11.7-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

ENV APP_ENV production

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9042"]

