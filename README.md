# ship-il-sdk

Production-grade Python SDK for SHIP Israel API.

Supports:

- DEV and PROD environments
- Sync + Async clients
- Automatic token refresh
- Structured logging
- Retries with exponential backoff
- Full Pydantic response parsing
- CI with GitHub Actions
- PyPI publishing
- Spec-driven, OpenAPI-style endpoint contracts

Install:

pip install -e .

Current endpoint coverage:

- Authentication via `/Token`
- `GET /api/v1/pickups/getclosestpoints`
- `POST /api/v1/shipments/drop-pickup-ex`
- `GET /api/v2/shipments/print/batch`

Generic shipment-preparation workflow:

1. Build a normalized consignee address with `build_consignee_address(...)`
2. Build a reusable shipment draft with `build_shipment_preparation(...)`
3. Fetch candidate pickup points with `client.points.get_closest_points(...)`
4. Either:
   - choose a point manually and call `build_pickup_shipment_request(...)`, or
   - use `recommend_pickup_point(...)` as a conservative heuristic
5. Submit the final request with `client.shipments.insert_pickup_shipment(...)`
