from typing import Optional

from .models.points import ClosestPointsResponse, PickupPoint
from .models.shipments import (
    ShipAddressInputModel,
    ShipmentPreparationInput,
    ShipmentRequest,
)


def build_consignee_address(
    *,
    city_name: str,
    street_name: str,
    house_number: str,
    contact_person: str,
    customer_name: str,
    phone1: str,
    city_code: Optional[int] = None,
    street_code: Optional[int] = None,
    location_description: Optional[str] = None,
    phone2: Optional[str] = None,
    room_number: Optional[str] = None,
    floor: Optional[str] = None,
    zip_code: Optional[str] = None,
) -> ShipAddressInputModel:
    return ShipAddressInputModel(
        CityName=city_name,
        StreetName=street_name,
        HouseNumber=str(house_number),
        ContactPerson=contact_person,
        CustomerName=customer_name,
        Phone1=phone1,
        CityCode=city_code,
        StreetCode=street_code,
        LocationDescription=location_description,
        Phone2=phone2,
        RoomNumber=room_number,
        Floor=floor,
        ZipCode=zip_code,
    )


def build_shipment_preparation(
    *,
    consignee_address: ShipAddressInputModel,
    number_of_packages: int = 1,
    shipper_address: Optional[ShipAddressInputModel] = None,
    reference1: Optional[str] = None,
    reference2: Optional[str] = None,
    shipment_instructions: Optional[str] = None,
    use_default_shipper_address: bool = True,
    context_customer_id: Optional[int] = None,
    context_user_email: Optional[str] = None,
    user_display_name: Optional[str] = None,
    original_data: Optional[str] = None,
) -> ShipmentPreparationInput:
    return ShipmentPreparationInput(
        ConsigneeAddress=consignee_address,
        ShipperAddress=shipper_address,
        Reference1=reference1,
        Reference2=reference2,
        ShipmentInstructions=shipment_instructions,
        UseDefaultShipperAddress=use_default_shipper_address,
        NumberOfPackages=number_of_packages,
        ContextCustomerID=context_customer_id,
        ContextUserEmail=context_user_email,
        UserDisplayName=user_display_name,
        OriginalData=original_data,
    )


def build_pickup_shipment_request(
    *,
    preparation: ShipmentPreparationInput,
    pickup_point_id: str,
    pickup_point_type: str,
) -> ShipmentRequest:
    return ShipmentRequest(
        **preparation.model_dump(),
        PickupPointID=str(pickup_point_id),
        PickupPointType=str(pickup_point_type),
    )


def build_pickup_shipment_request_from_point(
    *,
    preparation: ShipmentPreparationInput,
    pickup_point: PickupPoint,
) -> ShipmentRequest:
    return build_pickup_shipment_request(
        preparation=preparation,
        pickup_point_id=str(pickup_point.PointID),
        pickup_point_type=str(pickup_point.PointType),
    )


def recommend_pickup_point(
    response: ClosestPointsResponse,
    *,
    max_distance_km: float = 0.5,
    min_distance_gap_km: float = 1.0,
) -> Optional[PickupPoint]:
    if not response.IsSuccessful or not response.Points:
        return None

    first = response.Points[0]
    first_distance = first.Distance
    if first_distance is None or first_distance > max_distance_km:
        return None

    if len(response.Points) == 1:
        return first

    second_distance = response.Points[1].Distance
    if second_distance is None:
        return first

    if second_distance - first_distance >= min_distance_gap_km:
        return first

    return None
