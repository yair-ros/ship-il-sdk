# ship-il-sdk

[![PyPI version](https://img.shields.io/pypi/v/ship-il-sdk.svg)](https://pypi.org/project/ship-il-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/ship-il-sdk.svg)](https://pypi.org/project/ship-il-sdk/)
[![License](https://img.shields.io/pypi/l/ship-il-sdk.svg)](LICENSE)
[![CI](https://github.com/yair-ros/ship-il-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/yair-ros/ship-il-sdk/actions/workflows/ci.yml)

Independent/community Python SDK for the SHIP Israel API.

This is not an official SHIP SDK. It is an independent/community project.

PyPI: <https://pypi.org/project/ship-il-sdk/>

## Documentation

- [Usage guide](https://github.com/yair-ros/ship-il-sdk/blob/main/docs/usage.md): how to use this Python SDK.
- [SDK API reference](https://github.com/yair-ros/ship-il-sdk/blob/main/docs/api.md): Python classes, methods, return values, and exceptions.
- [OpenAPI contract](https://github.com/yair-ros/ship-il-sdk/blob/main/docs/openapi.yaml): raw SHIP HTTP API contract for the endpoints currently wrapped by this SDK.
- [SHIP Authentication wiki](https://wiki.ship.co.il/en/api/Authentication)
- [SHIP Shipments wiki](https://wiki.ship.co.il/en/api/Shipments)
- [SHIP Booking wiki](https://wiki.ship.co.il/en/api/Booking)
- [Contributing guide](https://github.com/yair-ros/ship-il-sdk/blob/main/CONTRIBUTING.md)
- [Changelog](https://github.com/yair-ros/ship-il-sdk/blob/main/CHANGELOG.md)
- [Security policy](https://github.com/yair-ros/ship-il-sdk/blob/main/SECURITY.md)

The OpenAPI file documents the vendor HTTP endpoints, not the Python SDK itself.
It is included as a reference for API tooling, contract review, mock servers, or
future code generation. The SDK does not load it at runtime.

## Installation

From PyPI:

```bash
python -m pip install ship-il-sdk
```

From this repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

If you only want to run from a checkout without installing:

```bash
PYTHONPATH=src python -m pytest -q
```

## Development

Install the SDK and dev tooling inside a virtual environment:

```bash
make install
```

Available commands:

```bash
make format
make lint
make typecheck
make test
make check
make integration-test
make package
make release
```

`make package` builds the source distribution and wheel into `dist/`.
`make release` increments the latest `vX.Y.Z` tag by one patch version, updates
`pyproject.toml`, runs verification, commits the version bump, creates an
annotated tag, pushes the branch, and pushes the tag.
`make check` runs lint, typecheck, and tests.
`make integration-test` runs the real API integration script.

## CI/CD

GitHub Actions workflows live in `.github/workflows/`.

- `ci.yml` runs on pull requests to `main` and manual dispatch. It installs the
  package with dev tooling, then runs lint, typecheck, and tests across Python
  3.9 through 3.13, and builds the package once on Python 3.13.
- `release.yml` runs only on tags matching `v*`. It runs the same checks,
  builds `dist/`, uploads the distribution files as a workflow artifact,
  creates a GitHub Release, and publishes to PyPI through Trusted Publishing.
- PyPI publishing does not use a stored API token. Configure a pending trusted
  publisher in PyPI with these values:
  - PyPI project name: `ship-il-sdk`
  - Owner: `yair-ros`
  - Repository name: `ship-il-sdk`
  - Workflow name: `release.yml`
  - Environment name: `pypi`

To create a GitHub Release and trigger PyPI publishing:

```bash
make release
```

If your virtual environment is not activated, pass the interpreter explicitly:

```bash
make release PYTHON=.venv/bin/python
```

## Usage

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

Additional shipment operations currently exposed by the SDK:

- `insert_standard_shipment(...)`
- `insert_pickup_shipment(...)`
- `insert_pickup_drop_shipment(...)`
- `insert_picking_list(...)`
- `print_wb_order_details(...)`
- `get_wb_status(...)`
- `get_pricing(...)`

Booking operations currently exposed by the SDK:

- `get_pickup_dates(...)`
- `get_pickup_times(...)`
- `insert_domestic_booking(...)`
- `insert_export_booking(...)`
- `cancel_booking(...)`

The repository no longer keeps standalone example scripts under `examples/`.
Use `scripts/integration_test.py` for real DEV verification and `docs/usage.md`
for copy-paste SDK usage patterns.

## Supported Workflow

The SDK supports a generic flow that does not depend on any specific commerce
platform:

1. authenticate
2. find closest pickup points
3. build a shipment draft
4. manually or heuristically choose a pickup point
5. create the shipment
6. download the label

For conservative automatic recommendation, use `recommend_pickup_point(...)`.
If it returns `None`, require manual pickup selection.

## Official API References

The SDK implementation should be reviewed against the official SHIP docs:

- Authentication: [wiki.ship.co.il/en/api/Authentication](https://wiki.ship.co.il/en/api/Authentication)
- Shipments: [wiki.ship.co.il/en/api/Shipments](https://wiki.ship.co.il/en/api/Shipments)
- Booking: [wiki.ship.co.il/en/api/Booking](https://wiki.ship.co.il/en/api/Booking)

## Error Handling

```python
from ship_il_sdk import Environment, ShipClient
from ship_il_sdk.exceptions import AuthenticationError, ShipAPIError

client = ShipClient(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    customer_id="YOUR_CUSTOMER_ID",
    environment=Environment.DEV,
)

try:
    client.login()
except AuthenticationError as exc:
    print(f"Authentication failed: {exc}")

try:
    points = client.points.get_closest_points(
        city="Tel Aviv",
        street="Herzl",
        house_number="10",
    )
except ShipAPIError as exc:
    print(f"API error: {exc}")
```
