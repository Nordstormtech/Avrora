FROM python:3.10.1-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR usr/src/Avrora


RUN apt-get update \
    && apt-get -y install netcat gcc postgresql libpq-dev \
    && pip install --upgrade pip \
    && apt-get clean

# install python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/Avrora/entrypoint.sh


ENTRYPOINT ["/usr/src/Avrora/entrypoint.sh"]
#CMD ["sh", "entrypoint.sh"]