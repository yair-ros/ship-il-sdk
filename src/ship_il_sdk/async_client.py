import httpx

from .config import Environment
from .exceptions import ShipAPIError
from .logging import get_logger
from .token_manager import TokenManager
from .transport.parsing import parse_model
from .endpoints.specs import GET_CLOSEST_POINTS
from .models.points import ClosestPointsResponse


class AsyncShipClient:
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

        self.client = httpx.AsyncClient(timeout=timeout)
        self.token = None
        self.tokens = TokenManager()
        self.logger = get_logger().bind(
            client="async",
            environment=environment.name,
            base_url=self.base_url,
        )

    async def login(self):
        r = await self.client.post(
            f"{self.base_url}/Token",
            data={
                "username": self.username,
                "password": self.password,
                "scope": str(self.customer_id),
                "grant_type": "password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if r.status_code != 200:
            raise ShipAPIError(r.text)

        data = r.json()
        self.token = data.get("access_token")
        if not self.token:
            raise ShipAPIError("Token missing")

        self.tokens.set_token(self.token, ttl=int(data.get("expires_in", 3600)))
        self.client.headers["Authorization"] = f"Bearer {self.token}"
        self.logger.info("token_refreshed", expires_in=int(data.get("expires_in", 3600)))

    async def _ensure_token(self):
        if self.tokens.is_expired():
            await self.login()

    async def get_closest_points(
        self,
        city,
        street,
        house_number,
        point_types="1,2,4",
        points=10,
    ) -> ClosestPointsResponse:
        await self._ensure_token()

        r = await self.client.get(
            f"{self.base_url}{GET_CLOSEST_POINTS.path}",
            params={
                "city": city,
                "street": street,
                "houseNumber": house_number,
                "pointTypes": point_types,
                "points": points,
            },
        )

        if r.status_code >= 400:
            raise ShipAPIError(r.text)

        self.logger.info(
            "api_call",
            method=GET_CLOSEST_POINTS.method,
            endpoint=GET_CLOSEST_POINTS.path,
            status=r.status_code,
        )

        return parse_model(GET_CLOSEST_POINTS.response_model, r.json())
