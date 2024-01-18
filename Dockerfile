FROM python:3.9.2-slim-buster

WORKDIR /work

COPY --link requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install --requirement=requirements.txt

COPY --link . .
STOPSIGNAL SIGINT
CMD ["python3", "test.py"]
