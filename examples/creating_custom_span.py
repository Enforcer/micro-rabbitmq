import requests
from opentelemetry.sdk.trace import Span, Tracer

# =*= Creation of custom a span =*=

# from <service>.tracing import setup
# tracer = setup(service_name="Something")

tracer: Tracer

with tracer.start_as_current_span(name="<span name>") as span:
    span: Span
    span.add_event("Example", {"count": 1})  # put some extra data in the span
    requests.get("http://localhost:8000/endpoint")

# we assume RequestsInstrumentor has been called before (done by <service>.tracing)
