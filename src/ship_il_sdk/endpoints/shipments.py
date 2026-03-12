from .specs import INSERT_PICKUP_SHIPMENT


class ShipmentsAPI:
    def __init__(self, client):
        self.client = client

    def insert_pickup_shipment(self, shipment):
        if hasattr(shipment, "model_dump"):
            shipment = shipment.model_dump(exclude_none=True)
        elif hasattr(shipment, "dict"):
            shipment = shipment.dict(exclude_none=True)

        return self.client._request_model(
            INSERT_PICKUP_SHIPMENT,
            json=shipment,
        )
