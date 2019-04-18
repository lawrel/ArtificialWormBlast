FROM python:3.7-alpine

MAINTAINER Sean Rice "seane.rice@gmail.com"

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pipenv

COPY . /app

WORKDIR /app

RUN pipenv install --system --deploy --ignore-pipfile
# RUN pipenv shell

EXPOSE 80

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]