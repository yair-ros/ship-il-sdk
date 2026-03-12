import structlog

_CONFIGURED = False


def get_logger():
    global _CONFIGURED

    if not _CONFIGURED:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.add_log_level,
                structlog.processors.JSONRenderer(),
            ]
        )
        _CONFIGURED = True

    return structlog.get_logger()
