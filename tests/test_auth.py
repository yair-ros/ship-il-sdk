import pytest

from ship_il_sdk.auth import DEFAULT_TIMEOUT, authenticate
from ship_il_sdk.client import ShipClient
from ship_il_sdk.exceptions import AuthenticationError


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload if payload is not None else {}
        self.text = text

    def json(self):
        return self._payload


class FakeSession:
    """Minimal stand-in for ``requests.Session`` that records calls."""

    def __init__(self, token_response=None):
        self.headers = {}
        self.post_calls = []
        self.request_calls = []
        self._token_response = token_response or FakeResponse(
            payload={"access_token": "tok", "expires_in": 3600}
        )

    def post(self, url, **kwargs):
        self.post_calls.append((url, kwargs))
        return self._token_response

    def request(self, method, url, **kwargs):
        self.request_calls.append((method, url, kwargs))
        return FakeResponse(payload={})


def _make_client(**kwargs):
    client = ShipClient(username="user", password="pass", customer_id="1", **kwargs)
    client.session = FakeSession()
    return client


def test_authenticate_uses_default_timeout():
    session = FakeSession()

    token, expires_in = authenticate(session, "https://host", "u", "p", "1")

    assert token == "tok"
    assert expires_in == 3600
    assert session.headers["Authorization"] == "Bearer tok"
    [(url, kwargs)] = session.post_calls
    assert url == "https://host/Token"
    assert kwargs["timeout"] == DEFAULT_TIMEOUT


def test_authenticate_passes_custom_timeout():
    session = FakeSession()

    authenticate(session, "https://host", "u", "p", "1", timeout=5)

    [(_, kwargs)] = session.post_calls
    assert kwargs["timeout"] == 5


def test_authenticate_preserves_existing_error_behavior():
    session = FakeSession(token_response=FakeResponse(status_code=401, text="denied"))

    with pytest.raises(AuthenticationError):
        authenticate(session, "https://host", "u", "p", "1", timeout=5)


def test_client_default_timeout_matches_authenticate_default():
    client = _make_client()

    assert client.timeout == DEFAULT_TIMEOUT


def test_login_passes_client_default_timeout_to_auth_request():
    client = _make_client()

    client.login()

    [(_, kwargs)] = client.session.post_calls
    assert kwargs["timeout"] == DEFAULT_TIMEOUT


def test_login_passes_custom_client_timeout_to_auth_request():
    client = _make_client(timeout=7)

    client.login()

    [(_, kwargs)] = client.session.post_calls
    assert kwargs["timeout"] == 7


def test_automatic_login_on_request_uses_client_timeout():
    client = _make_client(timeout=9)
    assert client.tokens.is_expired()

    client._request("GET", "/api/v1/anything")

    [(_, auth_kwargs)] = client.session.post_calls
    assert auth_kwargs["timeout"] == 9
    [(_, _, api_kwargs)] = client.session.request_calls
    assert api_kwargs["timeout"] == 9


def test_token_refresh_after_expiry_uses_client_timeout():
    client = _make_client(timeout=11)
    client.login()
    assert len(client.session.post_calls) == 1

    # Force the token to look expired so the next request re-authenticates.
    client.tokens.expiry = 0

    client._request("GET", "/api/v1/anything")

    assert len(client.session.post_calls) == 2
    assert all(kwargs["timeout"] == 11 for _, kwargs in client.session.post_calls)
