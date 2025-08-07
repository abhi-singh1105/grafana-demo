from flask import Flask
from prometheus_client import Counter, generate_latest
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import logging
import sys
import os

app = Flask(__name__)

# Prometheus metric
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint"])

# Logging
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# OpenTelemetry Tracing
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "demo-app"}))
)
tracer = trace.get_tracer(__name__)

# Configure OTLP gRPC Exporter to Grafana Cloud Tempo
import base64

username = os.getenv("GRAFANA_CLOUD_USERNAME")
api_key = os.getenv("GRAFANA_CLOUD_API_KEY")
credentials = f"{username}:{api_key}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

otlp_exporter = OTLPSpanExporter(
    endpoint="https://otlp-gateway-prod-eu-west-2.grafana.net/v1/traces",
    headers={"authorization": f"Bearer {os.getenv('GRAFANA_CLOUD_API_KEY')}"
    },
#    insecure=False,
#    timeout=20
)
print("GRAFANA_CLOUD_API_KEY=", os.getenv("GRAFANA_CLOUD_API_KEY"))
print("GRAFANA_CLOUD_USERNAME=", os.getenv("GRAFANA_CLOUD_USERNAME"))

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)


FlaskInstrumentor().instrument_app(app)

@app.route("/")
def hello():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    with tracer.start_as_current_span("hello-handler"):
        return "Hello from Flask with tracing!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)