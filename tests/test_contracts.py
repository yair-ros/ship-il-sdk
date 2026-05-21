from ship_il_sdk.endpoints.specs import (
    CANCEL_BOOKING,
    DOWNLOAD_LABEL,
    GET_CLOSEST_POINT,
    GET_CLOSEST_POINTS,
    GET_PICKUP_DATES,
    GET_PICKUP_TIMES,
    GET_PRICING,
    GET_WB_STATUS,
    INSERT_DOMESTIC_BOOKING,
    INSERT_EXPORT_BOOKING,
    INSERT_PICKING_LIST,
    INSERT_PICKUP_DROP_SHIPMENT,
    INSERT_PICKUP_SHIPMENT,
    INSERT_STANDARD_SHIPMENT,
    PRINT_WB_ORDER_DETAILS,
)
from ship_il_sdk.models.booking import (
    CancelBookingResponse,
    ExportBookingResponse,
    PickupDatesResponse,
    PickupTimeOption,
)
from ship_il_sdk.models.points import ClosestPointsResponse
from ship_il_sdk.models.shipments import (
    FileResponse,
    LabelResponse,
    PickingListResponse,
    PricingResponse,
    ShipmentResponse,
    WbStatusResponse,
)


def test_endpoint_contract_response_models():
    assert GET_CLOSEST_POINTS.response_model is ClosestPointsResponse
    assert GET_CLOSEST_POINT.response_model is ClosestPointsResponse
    assert GET_PICKUP_DATES.response_model is PickupDatesResponse
    assert GET_PICKUP_TIMES.response_model == list[PickupTimeOption]
    assert INSERT_STANDARD_SHIPMENT.response_model is ShipmentResponse
    assert INSERT_PICKUP_SHIPMENT.response_model is ShipmentResponse
    assert INSERT_PICKUP_DROP_SHIPMENT.response_model is ShipmentResponse
    assert INSERT_DOMESTIC_BOOKING.response_model is None
    assert INSERT_EXPORT_BOOKING.response_model is ExportBookingResponse
    assert CANCEL_BOOKING.response_model is CancelBookingResponse
    assert INSERT_PICKING_LIST.response_model is PickingListResponse
    assert DOWNLOAD_LABEL.response_model is LabelResponse
    assert PRINT_WB_ORDER_DETAILS.response_model is FileResponse
    assert GET_WB_STATUS.response_model is WbStatusResponse
    assert GET_PRICING.response_model is PricingResponse
