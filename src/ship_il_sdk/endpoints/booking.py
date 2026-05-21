from .specs import (
    CANCEL_BOOKING,
    GET_PICKUP_DATES,
    GET_PICKUP_TIMES,
    INSERT_DOMESTIC_BOOKING,
    INSERT_EXPORT_BOOKING,
)


class BookingAPI:
    def __init__(self, client):
        self.client = client

    def _dump(self, payload):
        if hasattr(payload, "model_dump"):
            return payload.model_dump(exclude_none=True)
        if hasattr(payload, "dict"):
            return payload.dict(exclude_none=True)
        return payload

    def get_pickup_dates(self, **params):
        return self.client._request_model(
            GET_PICKUP_DATES,
            params=params,
        )

    def get_pickup_times(self, **params):
        return self.client._request_model(
            GET_PICKUP_TIMES,
            params=params,
        )

    def insert_domestic_booking(self, booking):
        return self.client._request_model(
            INSERT_DOMESTIC_BOOKING,
            json=self._dump(booking),
        )

    def insert_export_booking(self, booking):
        return self.client._request_model(
            INSERT_EXPORT_BOOKING,
            json=self._dump(booking),
        )

    def cancel_booking(self, booking):
        return self.client._request_model(
            CANCEL_BOOKING,
            json=self._dump(booking),
        )
