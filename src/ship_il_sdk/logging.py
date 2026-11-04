"""SDK-local structured logging; handlers and levels belong to the host."""

import logging
from typing import Any

import structlog

_LOGGER = logging.getLogger("ship_il_sdk")
_LOGGER.addHandler(logging.NullHandler())


class _SafeBoundLogger(structlog.stdlib.BoundLogger):
    # Explicitly declare the inherited runtime attribute for protocol checkers.
    _context: structlog.typing.Context

    def _proxy_to_logger(
        self,
        method_name: str,
        event: str | None = None,
        *event_args: str,
        **event_kw: Any,
    ) -> Any:
        try:
            return super()._proxy_to_logger(method_name, event, *event_args, **event_kw)
        except Exception:
            # A broken host handler/formatter must not interrupt an API call.
            # Do not attempt fallback output: windowed apps may have no streams.
            return None


def get_logger():
    # Set every configurable option explicitly to avoid inheriting the host's
    # structlog defaults. Never merge arbitrary host context (possibly secrets).
    return structlog.wrap_logger(
        _LOGGER,
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=_SafeBoundLogger,
        context_class=dict,
        cache_logger_on_first_use=True,
    )
