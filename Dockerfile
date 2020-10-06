FROM python:3.8.5-slim-buster

RUN apt-get update
RUN apt-get install -y git gcc python3-dev musl-dev libpq-dev netcat

RUN mkdir /app
COPY . /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV OAUTHLIB_INSECURE_TRANSPORT=1

RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5000

CMD ["bash", "entrypoint.sh"]