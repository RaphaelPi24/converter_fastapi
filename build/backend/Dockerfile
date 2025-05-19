FROM python:3.12-slim


#RUN apt-get update && apt-get install -y \
#    libpq-dev \
#    libcairo2 \
#    libcairo2-dev \
#    libpango-1.0-0 \
#    libpangocairo-1.0-0 \
#    libgdk-pixbuf2.0-0 \
#    libffi-dev \
#    && apt-get clean && rm -rf /var/lib/apt/lists/* \
RUN apt-get update && apt-get install -y \
    libcairo2-dev pkg-config python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY --chmod=775 build/backend/entrypoint.dev.sh /entrypoint.sh
COPY ./src .
COPY build/.env.production .env
EXPOSE 8000
CMD ["/entrypoint.sh"]