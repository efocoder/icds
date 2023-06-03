FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip install -U pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system

COPY . .

EXPOSE 8000

RUN chmod u+x setup.sh

ENTRYPOINT ["/app/setup.sh"]
