FROM python:3.12-slim

RUN apt-get update && apt-get -y upgrade \
    && apt-get install -y \
    libcairo2-dev pkg-config python3-dev ffmpeg

WORKDIR /app

COPY ./src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY --chmod=775 build/backend/entrypoint.dev.sh /entrypoint.sh
COPY ./src .
COPY build/.env.production .env
COPY ./tests_convertors /app/tests_convertors

EXPOSE 8000
CMD ["/entrypoint.sh"]