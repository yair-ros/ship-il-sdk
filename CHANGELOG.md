# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project uses SemVer.

## [Unreleased]

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
