FROM python:3.8-alpine

WORKDIR /usr/src/api
ADD requirements.txt .

RUN apk add --no-cache build-base mariadb-connector-c-dev
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]