"""OpenTelemetry OTLP setup."""
from typing import Optional
from loguru import logger
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from app.global_config import get_config

_tracer: Optional[trace.Tracer] = None


def setup_otel() -> None:
    """Setup OpenTelemetry tracing if configured."""
    cfg = get_config()
    endpoint = cfg.get("otel_exporter_otlp_endpoint")
    service_name = cfg.get("service_name", "nicegui-chatbot")
    if not endpoint:
        logger.info("OTLP endpoint not configured; telemetry disabled.")
        return
    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    global _tracer
    _tracer = trace.get_tracer(service_name)
    logger.info(f"OpenTelemetry OTLP tracing enabled: {endpoint}")


def get_tracer() -> Optional[trace.Tracer]:
    """Get the global tracer."""
    return _tracer
