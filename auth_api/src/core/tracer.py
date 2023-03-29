from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import Resource, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from src.core.config import jaeger_settings


def configure_tracer() -> None:
    resource = Resource(attributes={"SERVICE_NAME": "auth-service"})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=jaeger_settings.JAEGER_HOST,
                agent_port=jaeger_settings.JAEGER_PORT,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
