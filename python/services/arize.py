"""Arize tracing. Call init_arize() after load_dotenv(), before any LLM calls.

Usage:
    from services.arize import init_arize
    tp = init_arize()
    # ... LLM calls ...
    if tp:
        tp.force_flush()
        tp.shutdown()
"""

import logging
import os

logger = logging.getLogger("arize")

tracer_provider = None


def init_arize():
    global tracer_provider
    if tracer_provider is not None:
        return tracer_provider

    space_id = os.environ.get("ARIZE_SPACE_ID", "")
    api_key = os.environ.get("ARIZE_API_KEY", "")
    if not space_id or not api_key:
        logger.warning("ARIZE_SPACE_ID and ARIZE_API_KEY not set -- skipping tracing")
        return None

    from arize.otel import register
    from openinference.instrumentation.openai import OpenAIInstrumentor

    logging.getLogger("arize.otel").setLevel(logging.WARNING)
    logging.getLogger("opentelemetry").setLevel(logging.WARNING)

    tracer_provider = register(
        space_id=space_id,
        api_key=api_key,
        project_name="social-media",
    )
    OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
    logger.info("Arize tracing initialized (project: social-media)")
    return tracer_provider
