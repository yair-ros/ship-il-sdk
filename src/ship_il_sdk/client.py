import requests

from .config import Environment
from .auth import authenticate
from .token_manager import TokenManager
from .logging import get_logger
from .exceptions import ShipAPIError
from .transport.parsing import parse_model

from .endpoints.shipments import ShipmentsAPI
from .endpoints.points import PointsAPI
from .endpoints.labels import LabelsAPI


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

    def _request(self, method, endpoint, **kwargs):
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

        return r.json()

    def _request_model(self, spec, **kwargs):
        data = self._request(spec.method, spec.path, **kwargs)
        return parse_model(spec.response_model, data)
