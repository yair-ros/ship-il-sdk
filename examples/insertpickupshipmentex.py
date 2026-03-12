import os

from ship_il_sdk import Environment, ShipClient
from ship_il_sdk.models.shipments import ShipAddressInputModel, ShipmentRequest


client = ShipClient(
    username=os.environ["SHIP_API_USER"],
    password=os.environ["SHIP_API_PASSWORD"],
    customer_id=os.environ["SHIP_CUSTOMER_ID"],
    environment=Environment[os.environ.get("SHIP_ENV", "DEV").upper()],
)

shipment = ShipmentRequest(
    ConsigneeAddress=ShipAddressInputModel(
        CityName=os.environ["SHIP_CONSIGNEE_CITY"],
        StreetName=os.environ["SHIP_CONSIGNEE_STREET"],
        HouseNumber=os.environ["SHIP_CONSIGNEE_HOUSE_NUMBER"],
        ContactPerson=os.environ["SHIP_CONSIGNEE_CONTACT_PERSON"],
        CustomerName=os.environ["SHIP_CONSIGNEE_CUSTOMER_NAME"],
        Phone1=os.environ["SHIP_CONSIGNEE_PHONE"],
    ),
    Reference1=os.environ.get("SHIP_REFERENCE_1"),
    Reference2=os.environ.get("SHIP_REFERENCE_2"),
    ShipmentInstructions=os.environ.get("SHIP_SHIPMENT_INSTRUCTIONS"),
    UseDefaultShipperAddress=os.environ.get("SHIP_USE_DEFAULT_SHIPPER_ADDRESS", "true").lower()
    != "false",
    NumberOfPackages=int(os.environ.get("SHIP_NUMBER_OF_PACKAGES", "1")),
    PickupPointType=os.environ["SHIP_PICKUP_POINT_TYPE"],
    PickupPointID=os.environ["SHIP_PICKUP_POINT_ID"],
    ContextCustomerID=int(os.environ["SHIP_CUSTOMER_ID"]),
    ContextUserEmail=os.environ.get("SHIP_CONTEXT_USER_EMAIL"),
    UserDisplayName=os.environ.get("SHIP_USER_DISPLAY_NAME"),
    OriginalData=os.environ.get("SHIP_ORIGINAL_DATA"),
)

response = client.shipments.insert_pickup_shipment(shipment)

print(response.model_dump_json(indent=2))
