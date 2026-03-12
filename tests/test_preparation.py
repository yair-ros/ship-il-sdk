from ship_il_sdk import (
    build_consignee_address,
    build_pickup_shipment_request,
    build_pickup_shipment_request_from_point,
    build_shipment_preparation,
    recommend_pickup_point,
)
from ship_il_sdk.models.points import ClosestPointsResponse, PickupPoint


def test_build_pickup_shipment_request_manual_selection():
    consignee = build_consignee_address(
        city_name="Tel Aviv",
        street_name="Herzl",
        house_number="10",
        contact_person="Yair Rosenfeld",
        customer_name="Yair Rosenfeld",
        phone1="0500000000",
    )
    preparation = build_shipment_preparation(
        consignee_address=consignee,
        number_of_packages=2,
        reference1="ORDER-123",
        context_customer_id=648149,
    )

    shipment = build_pickup_shipment_request(
        preparation=preparation,
        pickup_point_id="PKPS734447",
        pickup_point_type="1",
    )

    assert shipment.ConsigneeAddress.CityName == "Tel Aviv"
    assert shipment.NumberOfPackages == 2
    assert shipment.PickupPointID == "PKPS734447"
    assert shipment.PickupPointType == "1"


def test_build_pickup_shipment_request_from_point():
    consignee = build_consignee_address(
        city_name="Tel Aviv",
        street_name="Herzl",
        house_number="10",
        contact_person="Yair Rosenfeld",
        customer_name="Yair Rosenfeld",
        phone1="0500000000",
    )
    preparation = build_shipment_preparation(consignee_address=consignee)
    point = PickupPoint(
        CityName="Tel Aviv",
        PointID="PKPS734447",
        PointType=1,
        PointNumber="734447",
        Distance=0.44,
    )

    shipment = build_pickup_shipment_request_from_point(
        preparation=preparation,
        pickup_point=point,
    )

    assert shipment.PickupPointID == "PKPS734447"
    assert shipment.PickupPointType == "1"


def test_recommend_pickup_point_returns_none_when_choice_is_ambiguous():
    response = ClosestPointsResponse(
        IsSuccessful=True,
        Points=[
            PickupPoint(
                CityName="Tel Aviv",
                PointID="PKPS1",
                PointType=1,
                Distance=0.4,
            ),
            PickupPoint(
                CityName="Tel Aviv",
                PointID="PKPS2",
                PointType=1,
                Distance=0.6,
            ),
        ],
    )

    assert recommend_pickup_point(response) is None


def test_recommend_pickup_point_returns_first_when_gap_is_clear():
    response = ClosestPointsResponse(
        IsSuccessful=True,
        Points=[
            PickupPoint(
                CityName="Tel Aviv",
                PointID="PKPS1",
                PointType=1,
                Distance=0.4,
            ),
            PickupPoint(
                CityName="Tel Aviv",
                PointID="PKPS2",
                PointType=1,
                Distance=2.0,
            ),
        ],
    )

    assert recommend_pickup_point(response).PointID == "PKPS1"
