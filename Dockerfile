FROM gcr.io/distroless/python3
WORKDIR /app
ADD . /app
ENTRYPOINT ["python", "-m", "prom_metrics_check"]
