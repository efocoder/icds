FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip install -U pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system

COPY . .

EXPOSE 8000

ENTRYPOINT ["/app/setup.sh"]
