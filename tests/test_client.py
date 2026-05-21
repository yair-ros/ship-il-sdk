import base64

import requests

from ship_il_sdk.client import ShipClient
from ship_il_sdk.endpoints.specs import PRINT_WB_ORDER_DETAILS
from ship_il_sdk.models.shipments import FileResponse


class DummyResponse:
    def __init__(self, content: bytes, content_type: str = "application/pdf"):
        self.content = content
        self.headers = {"Content-Type": content_type}

    def json(self):
        raise requests.exceptions.JSONDecodeError("bad json", "", 0)


def test_decode_file_response_from_binary_payload():
    client = ShipClient(
        username="user",
        password="pass",
        customer_id="1",
    )

    payload = client._decode_response_for_model(
        FileResponse,
        DummyResponse(b"%PDF-1.4"),
    )

    assert payload["MediaType"] == "application/pdf"
    assert base64.b64decode(payload["FileByteArray"]) == b"%PDF-1.4"
    assert payload["FileName"] is None


def test_request_model_uses_binary_fallback_for_file_response():
    client = ShipClient(
        username="user",
        password="pass",
        customer_id="1",
    )
    client._request_response = lambda *args, **kwargs: DummyResponse(b"%PDF-1.4")

    response = client._request_model(
        PRINT_WB_ORDER_DETAILS,
        params={"trackingNumbers": "WB1"},
    )

    assert isinstance(response, FileResponse)
    assert response.file_bytes() == b"%PDF-1.4"
