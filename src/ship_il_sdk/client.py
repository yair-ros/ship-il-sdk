import base64

import requests

from .auth import authenticate
from .config import Environment
from .endpoints.booking import BookingAPI
from .endpoints.labels import LabelsAPI
from .endpoints.points import PointsAPI
from .endpoints.shipments import ShipmentsAPI
from .exceptions import ShipAPIError
from .logging import get_logger
from .token_manager import TokenManager
from .transport.parsing import parse_model


class ShipClient:
    def __init__(
        self,
        username,
        password,
        customer_id,
        environment=Environment.PROD,
        timeout=30,
    ):
        self.username = username
        self.password = password
        self.customer_id = customer_id
        self.base_url = environment.value
        self.timeout = timeout

        self.session = requests.Session()
        self.tokens = TokenManager()
        self.logger = get_logger().bind(
            client="sync",
            environment=environment.name,
            base_url=self.base_url,
        )

        self.shipments = ShipmentsAPI(self)
        self.bookings = BookingAPI(self)
        self.points = PointsAPI(self)
        self.labels = LabelsAPI(self)

    def login(self):
        token, expires_in = authenticate(
            self.session,
            self.base_url,
            self.username,
            self.password,
            self.customer_id,
        )

        self.tokens.set_token(token, ttl=expires_in)
        self.logger.info("token_refreshed", expires_in=expires_in)

    def _ensure_token(self):
        if self.tokens.is_expired():
            self.login()

    def _request_response(self, method, endpoint, **kwargs):
        self._ensure_token()

        r = self.session.request(
            method,
            f"{self.base_url}{endpoint}",
            timeout=self.timeout,
            **kwargs,
        )

        if r.status_code >= 400:
            raise ShipAPIError(r.text)

        self.logger.info(
            "api_call",
            method=method,
            endpoint=endpoint,
            status=r.status_code,
        )

        return r

    def _request(self, method, endpoint, **kwargs):
        return self._request_response(method, endpoint, **kwargs).json()

    def _request_model(self, spec, **kwargs):
        response = self._request_response(spec.method, spec.path, **kwargs)
        data = self._decode_response_for_model(spec.response_model, response)
        if spec.response_model is None:
            return data
        return parse_model(spec.response_model, data)

    def _decode_response_for_model(self, response_model, response):
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            if response_model is None:
                raise
            if hasattr(response_model, "model_fields"):
                field_names = set(response_model.model_fields)
                if {"MediaType", "FileByteArray"}.issubset(field_names):
                    return {
                        "MediaType": response.headers.get(
                            "Content-Type",
                            "application/octet-stream",
                        ),
                        "FileByteArray": base64.b64encode(response.content).decode(
                            "ascii"
                        ),
                        "FileName": None,
                    }
            raise
