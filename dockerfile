FROM python:3.12-alpine

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG APP_NAME=bus_app
ENV APP_NAME=${APP_NAME}
# WORKDIR /${APP_NAME}

ARG SERVER_PORT=8000
ARG SERVER_HOST=0.0.0.0

ENV SERVER_PORT=${SERVER_PORT}
ENV SERVER_HOST=${SERVER_HOST}

EXPOSE ${SERVER_PORT}

CMD ["sh", "-c", "exec uvicorn \"$APP_NAME\":app --host \"$SERVER_HOST\" --port \"$SERVER_PORT\""]