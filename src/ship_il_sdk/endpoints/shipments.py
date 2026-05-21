from .specs import (
    GET_PRICING,
    GET_WB_STATUS,
    INSERT_PICKING_LIST,
    INSERT_PICKUP_DROP_SHIPMENT,
    INSERT_PICKUP_SHIPMENT,
    INSERT_STANDARD_SHIPMENT,
    PRINT_WB_ORDER_DETAILS,
)


class ShipmentsAPI:
    def __init__(self, client):
        self.client = client

    def _dump(self, payload):
        if hasattr(payload, "model_dump"):
            return payload.model_dump(exclude_none=True)
        if hasattr(payload, "dict"):
            return payload.dict(exclude_none=True)
        return payload

    def insert_standard_shipment(self, shipment):
        return self.client._request_model(
            INSERT_STANDARD_SHIPMENT,
            json=self._dump(shipment),
        )

    def insert_pickup_shipment(self, shipment):
        return self.client._request_model(
            INSERT_PICKUP_SHIPMENT,
            json=self._dump(shipment),
        )

    def insert_pickup_drop_shipment(self, shipment):
        return self.client._request_model(
            INSERT_PICKUP_DROP_SHIPMENT,
            json=self._dump(shipment),
        )

    def insert_picking_list(self, payload):
        return self.client._request_model(
            INSERT_PICKING_LIST,
            json=self._dump(payload),
        )

    def print_wb_order_details(self, **params):
        return self.client._request_model(
            PRINT_WB_ORDER_DETAILS,
            params=params,
        )

    def get_wb_status(self, **params):
        return self.client._request_model(
            GET_WB_STATUS,
            params=params,
        )

    def get_pricing(self, payload):
        return self.client._request_model(
            GET_PRICING,
            json=self._dump(payload),
        )
