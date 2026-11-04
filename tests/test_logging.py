import asyncio
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import textwrap
from unittest import TestCase
from unittest.mock import Mock, patch

import pytest


def _exercise_clients():
    """Exercise every SDK logging site, including automatic token refresh."""
    import httpx

    from ship_il_sdk import AsyncShipClient, ShipClient

    credentials = {
        "username": "private-user",
        "password": "private-password",
        "customer_id": "private-customer",
    }
    token = {"access_token": "private-token", "expires_in": 3600}
    points = {"IsSuccessful": True, "Points": []}
    response = Mock(status_code=200)
    response.json.return_value = token
    api_response = Mock(status_code=200)
    api_response.json.return_value = points

    with patch("requests.Session") as session_factory:
        session = session_factory.return_value
        session.post.return_value = response
        session.request.return_value = api_response
        client = ShipClient(**credentials)
        for _ in range(2):
            client.tokens.expiry = 0
            assert client.points.get_closest_points("City", "Street", "1").Points == []
        assert session.post.call_count == 2
        assert session.request.call_count == 2

    async def exercise_async():
        client = AsyncShipClient(**credentials)
        await client.client.aclose()

        def respond(request):
            payload = token if request.url.path == "/Token" else points
            return httpx.Response(200, json=payload)

        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http:
            client.client = http
            for _ in range(2):
                client.tokens.expiry = 0
                result = await client.get_closest_points("City", "Street", "1")
                assert result.Points == []

    asyncio.run(exercise_async())


def _run_subprocess(script):
    src = str(Path(__file__).resolve().parents[1] / "src")
    env = dict(os.environ, PYTHONPATH=src)
    result = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(script)],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("host_handler", [False, True])
def test_windowed_app_without_standard_streams(host_handler):
    # Import structlog/SDK only AFTER removing the streams: PrintLogger binds
    # stdout at import time, so an in-process monkeypatch misses the regression.
    _run_subprocess(
        f"""
        import sys
        sys.stdout = sys.stderr = None
        import logging
        import runpy
        import structlog

        assert not structlog.is_configured()
        before = structlog.get_config().copy()
        logger = logging.getLogger("ship_il_sdk")
        logger.setLevel(logging.INFO)
        if {host_handler!r}:
            logger.addHandler(logging.StreamHandler())
        namespace = runpy.run_path({str(Path(__file__).resolve())!r})
        namespace["_exercise_clients"]()
        assert not structlog.is_configured()
        assert structlog.get_config() == before
        assert any(isinstance(h, logging.NullHandler) for h in logger.handlers)
        """
    )


def test_host_structlog_configuration_is_preserved():
    _run_subprocess(
        f"""
        import logging
        import runpy
        import structlog

        def forbidden(*args, **kwargs):
            raise AssertionError("SDK used host structlog configuration")

        structlog.configure(
            logger_factory=forbidden,
            processors=[forbidden],
            wrapper_class=forbidden,
            context_class=forbidden,
            cache_logger_on_first_use=False,
        )
        before = structlog.get_config().copy()
        import ship_il_sdk
        assert structlog.is_configured()
        assert structlog.get_config() == before
        records = []
        class Capture(logging.Handler):
            def emit(self, record):
                records.append(record)
        logger = logging.getLogger("ship_il_sdk")
        logger.addHandler(Capture())
        logger.setLevel(logging.INFO)
        namespace = runpy.run_path({str(Path(__file__).resolve())!r})
        namespace["_exercise_clients"]()
        assert len(records) == 8
        assert structlog.is_configured()
        assert structlog.get_config() == before
        """
    )


def test_logs_route_to_stdlib_without_credentials():
    import structlog

    # Even host-bound credentials must not be pulled into SDK log events.
    with structlog.contextvars.bound_contextvars(
        password="context-password",
        access_token="context-token",
        auth_payload={"password": "context-password"},
    ):
        with TestCase().assertLogs("ship_il_sdk", level="INFO") as captured:
            _exercise_clients()

    records = captured.records
    assert all(record.name == "ship_il_sdk" for record in records)
    events = [json.loads(record.getMessage()) for record in records]
    assert len(events) == 8
    for client in ("sync", "async"):
        client_events = [e for e in events if e["client"] == client]
        assert [e["event"] for e in client_events] == [
            "token_refreshed",
            "api_call",
            "token_refreshed",
            "api_call",
        ]
    assert all(record.levelno == logging.INFO for record in records)
    assert "private-" not in "\n".join(captured.output)
    assert "context-" not in "\n".join(captured.output)
    assert all(
        set(event)
        <= {
            "event",
            "client",
            "environment",
            "base_url",
            "timestamp",
            "level",
            "expires_in",
            "method",
            "endpoint",
            "status",
        }
        for event in events
    )


def test_logging_handler_failure_does_not_break_api_calls():
    class BrokenHandler(logging.Handler):
        def emit(self, record):
            raise RuntimeError("host log destination unavailable")

    logger = logging.getLogger("ship_il_sdk")
    handler = BrokenHandler()
    previous_level = logger.level
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    try:
        _exercise_clients()
    finally:
        logger.removeHandler(handler)
        logger.setLevel(previous_level)


def test_host_log_level_is_respected(caplog):
    with caplog.at_level(logging.WARNING, logger="ship_il_sdk"):
        _exercise_clients()
    assert not [r for r in caplog.records if r.name == "ship_il_sdk"]
