FROM python:3.9-buster AS base

WORKDIR /opt/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh .
COPY app app
ENV PYTHONPATH /opt/app

ENTRYPOINT ["./entrypoint.sh"]

FROM base AS api

COPY alembic.ini .
COPY alembic alembic

CMD ["api"]

FROM base AS worker

CMD ["worker"]

FROM base AS scheduler

CMD ["scheduler"]
