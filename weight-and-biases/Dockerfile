FROM python:3.12-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9000

ENV APP_ENV production

CMD ["wandb", "login", "$(cat /run/secrets/.env)"]