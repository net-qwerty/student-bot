FROM python:3.12-alpine

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
  	PIP_DISABLE_PIP_VERSION_CHECK=on \
  	PIP_DEFAULT_TIMEOUT=100


ENV TZ=Europe/Moscow
RUN apk add --no-cache tzdata && cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk add --no-cache \
    bash \
    build-base \
    git

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && pip freeze

COPY . ./

ENTRYPOINT ["python", "bot/app.py"]
