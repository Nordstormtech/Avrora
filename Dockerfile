FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR usr/src/Avrora_Leave
COPY . .

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk add --no-cache --upgrade bash \
    && chmod +x entrypoint.sh


CMD ["sh", "entrypoint.sh"]