from flask import Flask
from prometheus_client import Counter, generate_latest
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
import logging
import sys

app = Flask(__name__)

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint"])

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

trace.set_tracer_provider(TracerProvider())
span_exporter = OTLPSpanExporter(endpoint="http://alloy:4318/v1/traces")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(span_exporter))
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def hello():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    app.logger.info("Hello endpoint hit")
    with trace.get_tracer(__name__).start_as_current_span("hello-span"):
        return "Hello from Grafana demo app!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
