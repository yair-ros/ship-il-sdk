# Usage

This SDK wraps the SHIP Israel authentication, pickup-point, shipment, and
label endpoints.

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