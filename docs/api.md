# API Reference

## `ShipClient`

```python
from ship_il_sdk import Environment, ShipClient

client = ShipClient(
    username="...",
    password="...",
    customer_id="...",
    environment=Environment.PROD,
    timeout=30,
)
```

Creates a synchronous client for the SHIP Israel API.

Authentication uses:

```text
POST /Token
Content-Type: application/x-www-form-urlencoded
```

## `AsyncShipClient`

```python
from ship_il_sdk import AsyncShipClient, Environment

client = AsyncShipClient(
    username="...",
    password="...",
    customer_id="...",
    environment=Environment.PROD,
    timeout=30,
)
```

Creates an asynchronous client for SHIP.

## Endpoints

### `client.points.get_closest_points(...)`

Calls:

```text
GET /api/v1/pickups/getclosestpoints
```

Returns `ClosestPointsResponse`.

### `client.shipments.insert_pickup_shipment(...)`

Calls:

```text
POST /api/v1/shipments/drop-pickup-ex
```

Accepts `ShipmentRequest`.

Returns `ShipmentResponse`.

### `client.labels.download_label(...)`

Calls:

```text
GET /api/v2/shipments/print/batch
```

Returns `LabelResponse`.

## Generic Preparation Helpers

### `build_consignee_address(...)`

Builds `ShipAddressInputModel`.

### `build_shipment_preparation(...)`

Builds `ShipmentPreparationInput`, which is a reusable draft before pickup
selection.

### `build_pickup_shipment_request(...)`

Adds `PickupPointID` and `PickupPointType` to a draft and returns a final
`ShipmentRequest`.

### `build_pickup_shipment_request_from_point(...)`

Same as above, but reads the pickup-point fields from a `PickupPoint`.

### `recommend_pickup_point(...)`

Returns a conservative recommended `PickupPoint` or `None`.

## Exceptions

- `AuthenticationError`: auth call failed or token was missing
- `ShipAPIError`: API returned a non-success HTTP response
