FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY python-app/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install --user --no-warn-script-location -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY python-app/src/worksbyworrell /app/worksbyworrell
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
ENTRYPOINT ["python", "-m", "worksbyworrell.warlock.main"]
