from ship_il_sdk.models.booking import (
    CancelBookingResponse,
    ExportBookingResponse,
    PickupDatesResponse,
    PickupTimeOption,
)
from ship_il_sdk.models.shipments import (
    FileResponse,
    LabelResponse,
    PickingListResponse,
    PricingResponse,
    ShipAddressInputModel,
    ShipmentResponse,
    StandardAddressInputModel,
    StandardShipmentRequest,
    WbStatusResponse,
)
from ship_il_sdk.token_manager import TokenManager


def test_label_response_decodes_bytes():
    label = LabelResponse(
        MediaType="application/pdf",
        FileByteArray="aGVsbG8=",
        FileName="label.pdf",
    )

    assert label.file_bytes() == b"hello"


def test_pickup_dates_response_parses():
    response = PickupDatesResponse.model_validate(
        {
            "Dates": [{"Id": "21/05/2026", "Title": "Thursday - 21/05/2026"}],
            "ErrorMessage": None,
        }
    )

    assert response.Dates[0].Id == "21/05/2026"


def test_pickup_time_option_parses():
    option = PickupTimeOption.model_validate(
        {
            "FromTime": "08:00",
            "ToTime": "16:50",
            "ServiceType": 31,
            "Free": False,
        }
    )

    assert option.ServiceType == 31
    assert option.Free is False


def test_export_booking_response_parses():
    response = ExportBookingResponse.model_validate(
        {"BookingNumber": "312312", "Error": ""}
    )

    assert response.BookingNumber == "312312"


def test_cancel_booking_response_parses_string_success():
    response = CancelBookingResponse.model_validate(
        {"IsSuccess": "true", "Error": ""}
    )

    assert response.IsSuccess is True


def test_file_response_decodes_bytes_without_filename():
    document = FileResponse(MediaType="application/pdf", FileByteArray="aGVsbG8=")

    assert document.file_bytes() == b"hello"
    assert document.FileName is None


def test_token_manager_refreshes_before_hard_expiry():
    tokens = TokenManager(refresh_margin=60)
    tokens.set_token("secret", ttl=30)

    assert tokens.is_expired() is True


def test_standard_shipment_request_defaults():
    shipment = StandardShipmentRequest(
        Weight=1.5,
        NumberOfPackages=1,
        ConsigneeAddress=StandardAddressInputModel(
            CustomerName="Test Customer",
            CityName="Tel Aviv",
            ContactPerson="Test Customer",
            StreetName="Herzl",
            Phone="1234567",
            PhonePrefix="054",
            Mobile="1234567",
            MobilePrefix="054",
            HouseNumber="10",
        ),
    )

    assert shipment.ShipmentType == 0
    assert shipment.NumberOfPackagesToReturn == 0
    assert shipment.DDO is False
    assert shipment.IsReturn is False
    assert shipment.UseDefaultShipperAddress is True


def test_wb_status_response_parses_documented_shape():
    response = WbStatusResponse.model_validate(
        {
            "Status": "נמסר",
            "DeliveredOn": "19/02/2019 16:55",
            "LeftAt": "UPS BEN GURION AIRPORT",
            "RecivedBy": "AMIT",
            "Receipent": None,
            "Weight": None,
            "Dispatch": None,
            "LastSite": "UPS BEN GURION AIRPORT",
            "Service": "Worldwide Services",
            "ShipmentProgress": [
                {
                    "Activity": "נמסר",
                    "LocalTime": "16:55",
                    "LocalDate": "19/02/2019",
                    "Location": "UPS BEN GURION AIRPORT, IL",
                }
            ],
        }
    )

    assert response.Status == "נמסר"
    assert response.ShipmentProgress[0].Activity == "נמסר"


def test_wb_status_response_coerces_null_progress():
    response = WbStatusResponse.model_validate({"Status": "Pending", "ShipmentProgress": None})

    assert response.ShipmentProgress == []


def test_pricing_response_parses_services_wrapper():
    response = PricingResponse.model_validate(
        {
            "ServicesPricing": [
                {
                    "Items": [
                        {
                            "Fee": "Base",
                            "FeeCode": "B",
                            "Price": 10.5,
                            "RowType": 1,
                        }
                    ],
                    "ServiceCode": 2,
                    "SeviceName": "Express",
                    "Days": 2,
                    "EstimatedDate": "2026-05-21",
                }
            ]
        }
    )

    assert response.ServicesPricing[0].ServiceCode == 2
    assert response.ServicesPricing[0].SeviceName == "Express"
    assert response.ServicesPricing[0].Items[0].Price == 10.5


def test_shipment_response_coerces_empty_tracking_lists():
    response = ShipmentResponse.model_validate(
        {
            "Result": {
                "PackageTrackingNumbers": [],
                "ReturnPackageTrackingNumbers": [],
                "ReturnTrackingNumber": [],
                "TrackingNumber": "WB123",
                "ErrorCode": 0,
                "ErrorMessage": "",
            }
        }
    )

    assert response.Result.ReturnTrackingNumber is None
    assert response.Result.TrackingNumber == "WB123"


def test_picking_list_response_parses():
    response = PickingListResponse.model_validate(
        {
            "ReturnValue": 1191,
            "ErrorDescription": "",
            "ErrorCode": 0,
        }
    )

    assert response.ReturnValue == 1191
    assert response.ErrorCode == 0


def test_pickup_address_model_keeps_phone1_shape():
    address = ShipAddressInputModel(
        CityName="Tel Aviv",
        StreetName="Herzl",
        HouseNumber="10",
        ContactPerson="Dana",
        CustomerName="Dana",
        Phone1="0501234567",
    )

    assert address.Phone1 == "0501234567"
