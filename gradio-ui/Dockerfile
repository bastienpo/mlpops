FROM python:3.11-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV APP_ENV production

CMD ["python", "app.py"]
