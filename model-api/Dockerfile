FROM python:3.11.7-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9042

ENV APP_ENV production

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9042"]
