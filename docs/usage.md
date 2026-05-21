# Usage

This SDK wraps the SHIP Israel authentication, pickup-point, shipment, and
label endpoints.

Official SHIP docs:

- [Authentication](https://wiki.ship.co.il/en/api/Authentication)
- [Shipments](https://wiki.ship.co.il/en/api/Shipments)
- [Booking](https://wiki.ship.co.il/en/api/Booking)

## Authenticate and Find Pickup Points

```python
from ship_il_sdk import Environment, ShipClient

client = ShipClient(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    customer_id="YOUR_CUSTOMER_ID",
    environment=Environment.DEV,
)

points = client.points.get_closest_points(
    city="Tel Aviv",
    street="Herzl",
    house_number="10",
)

print(points.Points[0].PointID)
```

## Booking Workflow

```python
from ship_il_sdk import (
    BookingAddress,
    BookingCustomerInfo,
    BookingRequest,
    Environment,
    ShipClient,
)

client = ShipClient(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    customer_id="YOUR_CUSTOMER_ID",
    environment=Environment.DEV,
)

dates = client.bookings.get_pickup_dates(
    CustomerNumber="YOUR_CUSTOMER_ID",
    CityName="Tel Aviv",
    StreetName="Herzl",
    ServiceType=31,
    Domestic=True,
    HolidayServiceType=1,
)

times = client.bookings.get_pickup_times(
    CityName="Tel Aviv",
    StreetName="Herzl",
    SelectedDay=dates.Dates[0].Id,
    ServiceType=31,
    Domestic=True,
)

booking = BookingRequest(
    ContactPerson="Dana Cohen",
    OpenBy="SDK",
    Weight=1.5,
    ServiceNumber=31,
    PackagesNumber=1,
    IsFlatPlace=False,
    ConfirmByMail=False,
    PickupToTime=times[0].ToTime,
    PickupFromTime=times[0].FromTime,
    PickupDate=dates.Dates[0].Id,
    CustomerInfo=BookingCustomerInfo(
        Address=BookingAddress(
            CustomerName="Dana Cohen",
            CityName="Tel Aviv",
            ContactPerson="Dana Cohen",
            StreetName="Herzl",
            Phone="1234567",
            PhonePrefix="03",
            Mobile="1234567",
            MobilePrefix="050",
            HouseNumber="10",
        )
    ),
    PackageType=2,
)

booking_number = client.bookings.insert_domestic_booking(booking)
print(booking_number)
```

## Create a Pickup Shipment

```python
from ship_il_sdk import (
    Environment,
    ShipClient,
    build_consignee_address,
    build_pickup_shipment_request_from_point,
    build_shipment_preparation,
)

client = ShipClient(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    customer_id="YOUR_CUSTOMER_ID",
    environment=Environment.DEV,
)

points = client.points.get_closest_points(
    city="Tel Aviv",
    street="Herzl",
    house_number="10",
)

consignee = build_consignee_address(
    city_name="Tel Aviv",
    street_name="Herzl",
    house_number="10",
    contact_person="Dana Cohen",
    customer_name="Dana Cohen",
    phone1="0501234567",
)

preparation = build_shipment_preparation(
    consignee_address=consignee,
    number_of_packages=1,
    reference1="ORDER-123",
)

shipment = build_pickup_shipment_request_from_point(
    preparation=preparation,
    pickup_point=points.Points[0],
)

response = client.shipments.insert_pickup_shipment(shipment)
print(response.Result.TrackingNumber)
```

## Create a Pickup-Drop Shipment

```python
response = client.shipments.insert_pickup_drop_shipment(shipment)
print(response.Result.TrackingNumber)
```

## Create a Standard Shipment

```python
from ship_il_sdk import (
    Environment,
    ShipClient,
    StandardShipmentRequest,
    build_standard_address,
)

client = ShipClient(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    customer_id="YOUR_CUSTOMER_ID",
    environment=Environment.DEV,
)

standard = StandardShipmentRequest(
    Weight=1.5,
    NumberOfPackages=1,
    ConsigneeAddress=build_standard_address(
        city_name="Tel Aviv",
        street_name="Herzl",
        house_number="10",
        contact_person="Dana Cohen",
        customer_name="Dana Cohen",
        phone="1234567",
        phone_prefix="03",
        mobile="1234567",
        mobile_prefix="050",
    ),
    UseDefaultShipperAddress=True,
)

response = client.shipments.insert_standard_shipment(standard)
print(response.Result.TrackingNumber)
```

## Additional Shipments Endpoints

```python
status = client.shipments.get_wb_status(trackingNumber="YOUR_TRACKING_NUMBER")
details = client.shipments.print_wb_order_details(
    trackingNumbers="YOUR_TRACKING_NUMBER",
    isA4Format=False,
)
pricing = client.shipments.get_pricing(
    {
        "PackageType": 2,
        "IsExport": True,
        "ShipmentValue": 10,
        "ToZipCode": "10015",
        "ToCountryCode": "US",
        "ToCity": "New york",
        "Packages": [{"Length": 0, "Width": 0, "Height": 0, "Weight": 10}],
    }
)
```

## Download a Label

```python
from ship_il_sdk import Environment, ShipClient

client = ShipClient(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    customer_id="YOUR_CUSTOMER_ID",
    environment=Environment.DEV,
)

label = client.labels.download_label(
    tracking_number="YOUR_TRACKING_NUMBER",
    label_format="thermal",
)

with open(label.FileName, "wb") as handle:
    handle.write(label.file_bytes())
```

## Conservative Pickup Recommendation

```python
from ship_il_sdk import Environment, ShipClient, recommend_pickup_point

client = ShipClient(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    customer_id="YOUR_CUSTOMER_ID",
    environment=Environment.DEV,
)

points = client.points.get_closest_points(
    city="Tel Aviv",
    street="Herzl",
    house_number="10",
)

recommended = recommend_pickup_point(points)
if recommended is None:
    print("Manual pickup selection required")
```
