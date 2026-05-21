from ..models.booking import (
    CancelBookingResponse,
    ExportBookingResponse,
    PickupDatesResponse,
    PickupTimeOption,
)
from ..contracts import EndpointSpec
from ..models.points import ClosestPointsResponse
from ..models.shipments import (
    FileResponse,
    LabelResponse,
    PickingListResponse,
    PricingResponse,
    ShipmentResponse,
    WbStatusResponse,
)

GET_CLOSEST_POINTS = EndpointSpec(
    name="get_closest_points",
    method="GET",
    path="/api/v1/pickups/getclosestpoints",
    response_model=ClosestPointsResponse,
)

GET_PICKUP_DATES = EndpointSpec(
    name="get_pickup_dates",
    method="GET",
    path="/api/v1/pickups/dates-ex",
    response_model=PickupDatesResponse,
)

GET_PICKUP_TIMES = EndpointSpec(
    name="get_pickup_times",
    method="GET",
    path="/api/v1/pickups/time-ex",
    response_model=list[PickupTimeOption],
)

INSERT_PICKUP_SHIPMENT = EndpointSpec(
    name="insert_pickup_shipment",
    method="POST",
    path="/api/v1/shipments/insert-pickup-shipment-ex",
    response_model=ShipmentResponse,
)

INSERT_DOMESTIC_BOOKING: EndpointSpec[None] = EndpointSpec(
    name="insert_domestic_booking",
    method="POST",
    path="/api/v3/pickups/insert/pickup/domestic",
    response_model=None,
)

INSERT_EXPORT_BOOKING = EndpointSpec(
    name="insert_export_booking",
    method="POST",
    path="/api/v4/pickups/insert/pickup/export",
    response_model=ExportBookingResponse,
)

CANCEL_BOOKING = EndpointSpec(
    name="cancel_booking",
    method="DELETE",
    path="/api/v3/pickups/cancel/pickup",
    response_model=CancelBookingResponse,
)

INSERT_PICKUP_DROP_SHIPMENT = EndpointSpec(
    name="insert_pickup_drop_shipment",
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

INSERT_STANDARD_SHIPMENT = EndpointSpec(
    name="insert_standard_shipment",
    method="POST",
    path="/api/v1/shipments/insert-shipment-ex",
    response_model=ShipmentResponse,
)

INSERT_PICKING_LIST = EndpointSpec(
    name="insert_picking_list",
    method="POST",
    path="/api/v1/shipments/InsertPickingList",
    response_model=PickingListResponse,
)

PRINT_WB_ORDER_DETAILS = EndpointSpec(
    name="print_wb_order_details",
    method="GET",
    path="/api/v1/shipments/PrintWBOrderDetails",
    response_model=FileResponse,
)

GET_WB_STATUS = EndpointSpec(
    name="get_wb_status",
    method="GET",
    path="/api/v1/shipments/wb-status",
    response_model=WbStatusResponse,
)

GET_CLOSEST_POINT = EndpointSpec(
    name="get_closest_point",
    method="GET",
    path="/api/v1/pickups/getclosestpoint",
    response_model=ClosestPointsResponse,
)

GET_PRICING = EndpointSpec(
    name="get_pricing",
    method="POST",
    path="/api/v1/priceList/get-pricing",
    response_model=PricingResponse,
)
