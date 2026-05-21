# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project uses SemVer.

## [Unreleased]

## [0.2.3] - 2026-05-21

### Added

- Full `Booking` module support: `get_pickup_dates`, `get_pickup_times`, `insert_domestic_booking`, `insert_export_booking`, and `cancel_booking`
- New booking models: `BookingAddress`, `BookingCustomerInfo`, `BookingDateOption`, `BookingRequest`, `PickupDatesResponse`, `PickupTimeOption`, `ExportBookingResponse`, `CancelBookingRequest`, and `CancelBookingResponse`
- Booking integration flows in `scripts/integration_test.py`
- Binary-response fallback tests in `tests/test_client.py`

### Changed

- Removed the obsolete `examples/` scripts and their `Makefile` targets
- Aligned shipment and pricing contracts with the live SHIP API and official docs
- `parse_model(...)` now supports typed collection responses via Pydantic `TypeAdapter`
- `PrintWBOrderDetails` now supports binary payloads returned directly by SHIP instead of assuming JSON
- `WbStatusResponse` now tolerates `ShipmentProgress=null`

### Fixed

- Standard shipment requests now use the correct address schema with `Phone`, `PhonePrefix`, `Mobile`, and `MobilePrefix`
- Picking-list requests now use the documented `TrackNO` / `Items` payload shape
- Pricing responses now parse the documented `ServicesPricing` wrapper
- Shipment responses now tolerate `ReturnTrackingNumber=[]` from SHIP

## [0.2.0] - 2026-05-21

### Added

- New endpoints: `insert_standard_shipment`, `insert_pickup_drop_shipment`, `insert_picking_list`, `print_wb_order_details`, `get_wb_status`, `get_pricing`
- New models: `StandardAddressInputModel`, `StandardShipmentRequest`, `FileResponse`, `PickingListItem`, `PickingListRequest`, `PickingListResponse`, `WbStatusResponse`, `ShipmentProgressActivity`, `PricingPackage`, `PricingOption`, `PricingRequest`, `PricingResponse`
- `build_standard_address` helper for constructing `StandardAddressInputModel`
- Binary (non-JSON) response decoding for endpoints that return PDF/file content
- All new models and helpers exported from the top-level `ship_il_sdk` package

### Changed

- `INSERT_PICKUP_SHIPMENT` now correctly calls `/api/v1/shipments/insert-pickup-shipment-ex`; the former path (`/api/v1/shipments/drop-pickup-ex`) is now `INSERT_PICKUP_DROP_SHIPMENT`
- `LabelResponse` is now a subclass of `FileResponse`; `FileName` remains required on `LabelResponse` but is optional on `FileResponse`
- `ShipmentRequest` gained an optional `UseDefaultDestinationAddress` field

## [0.1.0] - 2026-05-20

### Added

- Initial Python SDK for the SHIP Israel API
- Sync and async clients
- Authentication, pickup-points lookup, pickup-shipment creation, and label download support
- Shipment-preparation helpers for building generic shipment drafts before pickup selection
- Unit tests, examples, CI, release workflow, and PyPI packaging
