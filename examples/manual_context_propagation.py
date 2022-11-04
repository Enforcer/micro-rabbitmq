from opentelemetry.trace import Tracer
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

# =*= Setting context from the outside =*=
tracer: Tracer

# lets assume 'headers' is a dictionary that contains 'traceparent' key
# with trace id inside.
headers = {
    "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01",
}
# This will be the case when we issue an http request within instrumented context.

propagator = TraceContextTextMapPropagator()
context = propagator.extract(
    carrier=headers
)  # we use propagator to extract trace info and build a context
with tracer.start_as_current_span(
    name="<span name>", context=context  # we pass context
) as span:
    pass


# =*= Extacting context to pass it further =*=
propagator = TraceContextTextMapPropagator()

# inside instrumented context, also automatically (e.g. inside FastAPI view)
with tracer.start_as_current_span(name="<span name>") as span:
    carrier = {}
    propagator.inject(carrier=carrier)  # grabs current context and puts it in the dict
