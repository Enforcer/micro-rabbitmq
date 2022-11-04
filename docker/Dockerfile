FROM python:3.10.4
WORKDIR /usr/src/app
RUN pip install poetry==1.2.2
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install
CMD [ "sleep", "infinity" ]
