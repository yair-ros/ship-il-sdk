from ship_il_sdk.endpoints.specs import (
    DOWNLOAD_LABEL,
    GET_CLOSEST_POINTS,
    INSERT_PICKUP_SHIPMENT,
)
from ship_il_sdk.models.points import ClosestPointsResponse
from ship_il_sdk.models.shipments import LabelResponse, ShipmentResponse


def test_endpoint_contract_response_models():
    assert GET_CLOSEST_POINTS.response_model is ClosestPointsResponse
    assert INSERT_PICKUP_SHIPMENT.response_model is ShipmentResponse
    assert DOWNLOAD_LABEL.response_model is LabelResponse
