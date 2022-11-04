FROM python:3.10.4
RUN apt-get update && apt-get install -y wget
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

WORKDIR /usr/src/app
RUN pip install poetry==1.2.2
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install
ENTRYPOINT ["dockerize", "-wait", "tcp://db:5432", "-wait", "http://rabbitmq:15672", "--timeout", "15s"]
CMD [ "sleep", "infinity" ]
