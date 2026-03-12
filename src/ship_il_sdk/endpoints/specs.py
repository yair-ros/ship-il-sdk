from ..contracts import EndpointSpec
from ..models.points import ClosestPointsResponse
from ..models.shipments import LabelResponse, ShipmentResponse

GET_CLOSEST_POINTS = EndpointSpec(
    name="get_closest_points",
    method="GET",
    path="/api/v1/pickups/getclosestpoints",
    response_model=ClosestPointsResponse,
)

INSERT_PICKUP_SHIPMENT = EndpointSpec(
    name="insert_pickup_shipment",
    method="POST",
    path="/api/v1/shipments/drop-pickup-ex",
    response_model=ShipmentResponse,
)

DOWNLOAD_LABEL = EndpointSpec(
    name="download_label",
    method="GET",
    path="/api/v2/shipments/print/batch",
    response_model=LabelResponse,
)
