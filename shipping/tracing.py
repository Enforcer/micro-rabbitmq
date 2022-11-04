from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.zipkin.proto.http import ZipkinExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import Tracer, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup(service_name: str, app: FastAPI) -> Tracer:
    resource = Resource(attributes={SERVICE_NAME: service_name})

    zipkin_exporter = ZipkinExporter(endpoint="http://zipkin:9411/api/v2/spans")

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(zipkin_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    RequestsInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument(enable_commenter=True, commenter_options={})
    FastAPIInstrumentor().instrument_app(app)

    return trace.get_tracer(__name__)
