from ship_il_sdk.endpoints.labels import LabelsAPI
from ship_il_sdk.endpoints.points import PointsAPI
from ship_il_sdk.endpoints.shipments import ShipmentsAPI
from ship_il_sdk.endpoints.specs import (
    DOWNLOAD_LABEL,
    GET_CLOSEST_POINTS,
    GET_PRICING,
    GET_WB_STATUS,
    INSERT_PICKING_LIST,
    INSERT_PICKUP_DROP_SHIPMENT,
    INSERT_PICKUP_SHIPMENT,
    INSERT_STANDARD_SHIPMENT,
    PRINT_WB_ORDER_DETAILS,
)
from ship_il_sdk.models.shipments import (
    PickingListRequest,
    PricingResponse,
    ShipAddressInputModel,
    ShipmentRequest,
    StandardAddressInputModel,
    StandardShipmentRequest,
)


class RecordingClient:
    def __init__(self):
        self.request_model_calls = []
        self.request_model_response = object()

    def _request_model(self, spec, **kwargs):
        self.request_model_calls.append((spec, kwargs))
        return self.request_model_response


def make_address() -> ShipAddressInputModel:
    return ShipAddressInputModel(
        CityName="Tel Aviv",
        StreetName="Herzl",
        HouseNumber="10",
        ContactPerson="Test Customer",
        CustomerName="Test Customer",
        Phone1="0501234567",
    )


def make_standard_address() -> StandardAddressInputModel:
    return StandardAddressInputModel(
        CustomerName="Test Customer",
        CityName="Tel Aviv",
        ContactPerson="Test Customer",
        StreetName="Herzl",
        Phone="1234567",
        PhonePrefix="054",
        Mobile="1234567",
        MobilePrefix="054",
        HouseNumber="10",
    )


def test_points_api_uses_expected_params():
    client = RecordingClient()
    api = PointsAPI(client)

    api.get_closest_points(
        city="Tel Aviv",
        street="Herzl",
        house_number="10",
        point_types="1,2",
        points=5,
    )

    assert client.request_model_calls == [
        (
            GET_CLOSEST_POINTS,
            {
                "params": {
                    "city": "Tel Aviv",
                    "street": "Herzl",
                    "houseNumber": "10",
                    "pointTypes": "1,2",
                    "points": 5,
                }
            },
        )
    ]


def test_labels_api_uses_expected_params():
    client = RecordingClient()
    api = LabelsAPI(client)

    api.download_label("TRACKING123", label_format="a4", copies=2)

    assert client.request_model_calls == [
        (
            DOWNLOAD_LABEL,
            {
                "params": {
                    "trackingNumber": "TRACKING123",
                    "labelFormat": "a4",
                    "copies": 2,
                }
            },
        )
    ]


def test_insert_pickup_shipment_dumps_pydantic_model():
    client = RecordingClient()
    api = ShipmentsAPI(client)
    shipment = ShipmentRequest(
        ConsigneeAddress=make_address(),
        NumberOfPackages=1,
        PickupPointType="1",
        PickupPointID="PKPS123",
    )

    api.insert_pickup_shipment(shipment)

    assert client.request_model_calls == [
        (
            INSERT_PICKUP_SHIPMENT,
            {
                "json": {
                    "ConsigneeAddress": {
                        "CityName": "Tel Aviv",
                        "StreetName": "Herzl",
                        "HouseNumber": "10",
                        "ContactPerson": "Test Customer",
                        "CustomerName": "Test Customer",
                        "Phone1": "0501234567",
                    },
                    "UseDefaultShipperAddress": True,
                    "NumberOfPackages": 1,
                    "PickupPointType": "1",
                    "PickupPointID": "PKPS123",
                }
            },
        )
    ]


def test_insert_pickup_drop_shipment_uses_drop_spec():
    client = RecordingClient()
    api = ShipmentsAPI(client)

    shipment = ShipmentRequest(
        ConsigneeAddress=make_address(),
        NumberOfPackages=1,
        PickupPointType="4",
        PickupPointID="PKP123456",
        UseDefaultDestinationAddress=True,
    )
    api.insert_pickup_drop_shipment(shipment)

    assert client.request_model_calls == [
        (
            INSERT_PICKUP_DROP_SHIPMENT,
            {
                "json": {
                    "ConsigneeAddress": {
                        "CityName": "Tel Aviv",
                        "StreetName": "Herzl",
                        "HouseNumber": "10",
                        "ContactPerson": "Test Customer",
                        "CustomerName": "Test Customer",
                        "Phone1": "0501234567",
                    },
                    "UseDefaultShipperAddress": True,
                    "NumberOfPackages": 1,
                    "PickupPointType": "4",
                    "PickupPointID": "PKP123456",
                    "UseDefaultDestinationAddress": True,
                }
            },
        )
    ]


def test_insert_standard_shipment_uses_standard_spec():
    client = RecordingClient()
    api = ShipmentsAPI(client)
    shipment = StandardShipmentRequest(
        Weight=1.5,
        NumberOfPackages=1,
        ConsigneeAddress=make_standard_address(),
    )

    api.insert_standard_shipment(shipment)

    assert client.request_model_calls == [
        (
            INSERT_STANDARD_SHIPMENT,
            {
                "json": {
                    "Weight": 1.5,
                    "ShipmentType": 0,
                    "NumberOfPackages": 1,
                    "NumberOfPackagesToReturn": 0,
                    "ConsigneeAddress": {
                        "CustomerName": "Test Customer",
                        "CityName": "Tel Aviv",
                        "ContactPerson": "Test Customer",
                        "StreetName": "Herzl",
                        "Phone": "1234567",
                        "PhonePrefix": "054",
                        "Mobile": "1234567",
                        "MobilePrefix": "054",
                        "HouseNumber": "10",
                    },
                    "DDO": False,
                    "IsReturn": False,
                    "UseDefaultShipperAddress": True,
                }
            },
        )
    ]


def test_insert_picking_list_uses_structured_request():
    client = RecordingClient()
    api = ShipmentsAPI(client)

    api.insert_picking_list(
        PickingListRequest(
            CustomerNumber=648149,
            Ref1="ORDER-123",
            TrackNO="WB1",
            Items=[],
        )
    )

    assert client.request_model_calls == [
        (
            INSERT_PICKING_LIST,
            {
                "json": {
                    "Items": [],
                    "CustomerNumber": 648149,
                    "Ref1": "ORDER-123",
                    "TrackNO": "WB1",
                }
            },
        )
    ]


def test_print_wb_order_details_uses_documented_params():
    client = RecordingClient()
    api = ShipmentsAPI(client)

    api.print_wb_order_details(trackingNumbers="WB1", isA4Format=False)

    assert client.request_model_calls == [
        (
            PRINT_WB_ORDER_DETAILS,
            {"params": {"trackingNumbers": "WB1", "isA4Format": False}},
        )
    ]


def test_get_wb_status_uses_documented_params():
    client = RecordingClient()
    api = ShipmentsAPI(client)

    api.get_wb_status(trackingNumber="WB1")

    assert client.request_model_calls == [
        (
            GET_WB_STATUS,
            {"params": {"trackingNumber": "WB1"}},
        )
    ]


def test_get_pricing_uses_response_model():
    client = RecordingClient()
    client.request_model_response = PricingResponse(ServicesPricing=[])
    api = ShipmentsAPI(client)

    response = api.get_pricing({"Weight": 1.5})

    assert client.request_model_calls == [
        (
            GET_PRICING,
            {"json": {"Weight": 1.5}},
        )
    ]
    assert isinstance(response, PricingResponse)
