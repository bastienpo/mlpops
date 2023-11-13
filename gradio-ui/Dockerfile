FROM python:3.12-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

ENV APP_ENV production

CMD ["python", "main.py"]