from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ship_il_sdk import (
    Environment,
    PickingListItem,
    PickingListRequest,
    PricingPackage,
    PricingRequest,
    ShipClient,
    StandardShipmentRequest,
    build_consignee_address,
    build_pickup_shipment_request,
    build_shipment_preparation,
    build_standard_address,
)
from ship_il_sdk.exceptions import AuthenticationError, ShipAPIError

ENV_FILE = Path(__file__).with_name("integration_test.env")
COLOR_RED = "\033[31m"
COLOR_YELLOW = "\033[33m"
COLOR_CYAN = "\033[36m"
COLOR_RESET = "\033[0m"
PLACEHOLDER_VALUES = {
    "SHIP_API_USER": {"YOUR_USERNAME"},
    "SHIP_API_PASSWORD": {"YOUR_PASSWORD"},
    "SHIP_CUSTOMER_ID": {"YOUR_CUSTOMER_ID"},
}


@dataclass(frozen=True)
class Config:
    username: str
    password: str
    customer_id: str
    environment: str
    city: str
    street: str
    house_number: str
    point_types: str
    points_limit: int
    run_insert_pickup_shipment: bool
    run_insert_pickup_drop_shipment: bool
    run_insert_standard_shipment: bool
    run_insert_picking_list: bool
    run_print_wb_order_details: bool
    run_get_wb_status: bool
    run_get_pricing: bool
    consignee_city: str | None
    consignee_street: str | None
    consignee_house_number: str | None
    consignee_contact_person: str | None
    consignee_customer_name: str | None
    consignee_phone: str | None
    pickup_point_type: str | None
    pickup_point_id: str | None
    pickup_drop_point_type: str | None
    pickup_drop_point_id: str | None
    reference_1: str | None
    reference_2: str | None
    shipment_instructions: str | None
    number_of_packages: int
    standard_weight: float
    standard_shipment_type: int
    standard_number_of_packages_to_return: int
    standard_ddo: bool
    standard_is_return: bool
    standard_udr_value: int | None
    standard_cod_value: float | None
    standard_instruction: str | None
    standard_pickup_point_id: str | None
    picking_list_payload: Any | None
    print_wb_order_details_params: dict[str, Any] | None
    wb_status_params: dict[str, Any] | None
    pricing_payload: Any | None
    run_download_label: bool
    tracking_number: str | None
    label_format: str
    label_copies: int
    label_output: str | None


def load_env_file(path: Path) -> dict[str, str]:
    if not path.is_file():
        print(f"Missing local config: {path}")
        print(
            "Create it from scripts/integration_test.env.example and fill your real values."
        )
        raise SystemExit(2)

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator:
            raise SystemExit(f"Invalid line in {path}: {raw_line}")
        cleaned = value.strip()
        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {'"', "'"}:
            cleaned = cleaned[1:-1]
        values[key.strip()] = cleaned
    return values


def required_value(values: dict[str, str], key: str) -> str:
    value = values.get(key, "").strip()
    if not value:
        raise SystemExit(f"Missing required value in {ENV_FILE.name}: {key}")
    placeholders = PLACEHOLDER_VALUES.get(key, set())
    if value in placeholders:
        raise SystemExit(
            f"Placeholder value still present in {ENV_FILE.name}: {key}={value}"
        )
    return value


def optional_value(values: dict[str, str], key: str) -> str | None:
    value = values.get(key, "").strip()
    return value or None


def bool_value(values: dict[str, str], key: str) -> bool:
    return values.get(key, "no").strip().lower() == "yes"


def json_value(values: dict[str, str], key: str) -> Any | None:
    value = optional_value(values, key)
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {ENV_FILE.name}: {key}: {exc}") from exc


def int_value(values: dict[str, str], key: str, default: int) -> int:
    return int(values.get(key, str(default)).strip())


def float_value(values: dict[str, str], key: str, default: float) -> float:
    return float(values.get(key, str(default)).strip())


def optional_int_value(values: dict[str, str], key: str) -> int | None:
    value = optional_value(values, key)
    return int(value) if value is not None else None


def optional_float_value(values: dict[str, str], key: str) -> float | None:
    value = optional_value(values, key)
    return float(value) if value is not None else None


def require_confirmation(values: dict[str, str]) -> None:
    if values.get("SHIP_CONFIRM_REAL_API_CALL") == "yes":
        return
    print(
        "This script calls the real SHIP API and may create a real shipment or label."
    )
    print(f"Edit {ENV_FILE.name} and set SHIP_CONFIRM_REAL_API_CALL=yes to run it.")
    raise SystemExit(2)


def load_config() -> Config:
    values = load_env_file(ENV_FILE)
    require_confirmation(values)
    return Config(
        username=required_value(values, "SHIP_API_USER"),
        password=required_value(values, "SHIP_API_PASSWORD"),
        customer_id=required_value(values, "SHIP_CUSTOMER_ID"),
        environment=values.get("SHIP_ENV", "DEV").strip().upper(),
        city=required_value(values, "SHIP_CITY"),
        street=required_value(values, "SHIP_STREET"),
        house_number=required_value(values, "SHIP_HOUSE_NUMBER"),
        point_types=values.get("SHIP_POINT_TYPES", "1,2,4").strip(),
        points_limit=int_value(values, "SHIP_POINTS_LIMIT", 10),
        run_insert_pickup_shipment=(
            bool_value(values, "SHIP_RUN_INSERT_PICKUP_SHIPMENT")
            or bool_value(values, "SHIP_RUN_CREATE_SHIPMENT")
        ),
        run_insert_pickup_drop_shipment=bool_value(
            values, "SHIP_RUN_INSERT_PICKUP_DROP_SHIPMENT"
        ),
        run_insert_standard_shipment=bool_value(
            values, "SHIP_RUN_INSERT_STANDARD_SHIPMENT"
        ),
        run_insert_picking_list=bool_value(values, "SHIP_RUN_INSERT_PICKING_LIST"),
        run_print_wb_order_details=bool_value(
            values, "SHIP_RUN_PRINT_WB_ORDER_DETAILS"
        ),
        run_get_wb_status=bool_value(values, "SHIP_RUN_GET_WB_STATUS"),
        run_get_pricing=bool_value(values, "SHIP_RUN_GET_PRICING"),
        consignee_city=optional_value(values, "SHIP_CONSIGNEE_CITY"),
        consignee_street=optional_value(values, "SHIP_CONSIGNEE_STREET"),
        consignee_house_number=optional_value(values, "SHIP_CONSIGNEE_HOUSE_NUMBER"),
        consignee_contact_person=optional_value(
            values, "SHIP_CONSIGNEE_CONTACT_PERSON"
        ),
        consignee_customer_name=optional_value(values, "SHIP_CONSIGNEE_CUSTOMER_NAME"),
        consignee_phone=optional_value(values, "SHIP_CONSIGNEE_PHONE"),
        pickup_point_type=optional_value(values, "SHIP_PICKUP_POINT_TYPE"),
        pickup_point_id=optional_value(values, "SHIP_PICKUP_POINT_ID"),
        pickup_drop_point_type=optional_value(values, "SHIP_PICKUP_DROP_POINT_TYPE"),
        pickup_drop_point_id=optional_value(values, "SHIP_PICKUP_DROP_POINT_ID"),
        reference_1=optional_value(values, "SHIP_REFERENCE_1"),
        reference_2=optional_value(values, "SHIP_REFERENCE_2"),
        shipment_instructions=optional_value(values, "SHIP_SHIPMENT_INSTRUCTIONS"),
        number_of_packages=int_value(values, "SHIP_NUMBER_OF_PACKAGES", 1),
        standard_weight=float_value(values, "SHIP_STANDARD_WEIGHT", 1.0),
        standard_shipment_type=int_value(values, "SHIP_STANDARD_SHIPMENT_TYPE", 0),
        standard_number_of_packages_to_return=int_value(
            values,
            "SHIP_STANDARD_NUMBER_OF_PACKAGES_TO_RETURN",
            0,
        ),
        standard_ddo=bool_value(values, "SHIP_STANDARD_DDO"),
        standard_is_return=bool_value(values, "SHIP_STANDARD_IS_RETURN"),
        standard_udr_value=optional_int_value(values, "SHIP_STANDARD_UDR_VALUE"),
        standard_cod_value=optional_float_value(values, "SHIP_STANDARD_COD_VALUE"),
        standard_instruction=optional_value(values, "SHIP_STANDARD_INSTRUCTION"),
        standard_pickup_point_id=optional_value(
            values, "SHIP_STANDARD_PICKUP_POINT_ID"
        ),
        picking_list_payload=json_value(values, "SHIP_PICKING_LIST_PAYLOAD_JSON"),
        print_wb_order_details_params=json_value(
            values,
            "SHIP_PRINT_WB_ORDER_DETAILS_PARAMS_JSON",
        ),
        wb_status_params=json_value(values, "SHIP_WB_STATUS_PARAMS_JSON"),
        pricing_payload=json_value(values, "SHIP_PRICING_PAYLOAD_JSON"),
        run_download_label=bool_value(values, "SHIP_RUN_DOWNLOAD_LABEL"),
        tracking_number=optional_value(values, "SHIP_TRACKING_NUMBER"),
        label_format=values.get("SHIP_LABEL_FORMAT", "thermal").strip(),
        label_copies=int_value(values, "SHIP_LABEL_COPIES", 1),
        label_output=optional_value(values, "SHIP_LABEL_OUTPUT"),
    )


def require_pickup_shipment_config(config: Config) -> None:
    required = {
        "SHIP_CONSIGNEE_CITY": config.consignee_city,
        "SHIP_CONSIGNEE_STREET": config.consignee_street,
        "SHIP_CONSIGNEE_HOUSE_NUMBER": config.consignee_house_number,
        "SHIP_CONSIGNEE_CONTACT_PERSON": config.consignee_contact_person,
        "SHIP_CONSIGNEE_CUSTOMER_NAME": config.consignee_customer_name,
        "SHIP_CONSIGNEE_PHONE": config.consignee_phone,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise SystemExit(
            f"Missing required shipment values in {ENV_FILE.name}: {', '.join(missing)}"
        )


def require_standard_shipment_config(config: Config) -> None:
    required = {
        "SHIP_CONSIGNEE_CITY": config.consignee_city,
        "SHIP_CONSIGNEE_STREET": config.consignee_street,
        "SHIP_CONSIGNEE_HOUSE_NUMBER": config.consignee_house_number,
        "SHIP_CONSIGNEE_CONTACT_PERSON": config.consignee_contact_person,
        "SHIP_CONSIGNEE_CUSTOMER_NAME": config.consignee_customer_name,
        "SHIP_CONSIGNEE_PHONE": config.consignee_phone,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise SystemExit(
            "Missing required standard-shipment values in "
            f"{ENV_FILE.name}: {', '.join(missing)}"
        )


def require_json_payload(name: str, payload: Any) -> None:
    if payload is None:
        raise SystemExit(f"Missing required JSON payload in {ENV_FILE.name}: {name}")


def require_json_object(name: str, payload: Any) -> dict[str, Any]:
    require_json_payload(name, payload)
    if not isinstance(payload, dict):
        raise SystemExit(f"{name} must be a JSON object in {ENV_FILE.name}.")
    return payload


def build_tracking_params(
    name: str,
    params: dict[str, Any] | None,
    tracking_number: str | None,
) -> dict[str, Any]:
    if params is not None:
        return require_json_object(name, params)
    if not tracking_number:
        raise SystemExit(
            f"{name} requires either explicit params JSON or a tracking number."
        )
    if name == "SHIP_PRINT_WB_ORDER_DETAILS_PARAMS_JSON":
        return {"trackingNumbers": tracking_number, "isA4Format": False}
    return {"trackingNumber": tracking_number}


def build_picking_list_payload(
    payload: Any | None,
    customer_id: str,
    reference_1: str | None,
    tracking_number: str | None,
) -> Any:
    if payload is not None:
        return payload
    if not tracking_number:
        raise SystemExit(
            "SHIP_PICKING_LIST_PAYLOAD_JSON requires either explicit JSON "
            "or a tracking number from an earlier shipment call."
        )
    return PickingListRequest(
        CustomerNumber=int(customer_id),
        Ref1=reference_1 or "SDK-INTEGRATION-TEST",
        TrackNO=tracking_number,
        Items=[
            PickingListItem(
                SKU1="231111",
                SKU2="1111",
                Description="Computer",
                Quantity=1,
                Location="B35-12",
                WH="",
                Remarks="integration test item",
            )
        ],
    )


def normalize_phone(phone: str) -> str:
    digits = "".join(ch for ch in phone if ch.isdigit())
    if digits.startswith("972"):
        digits = "0" + digits[3:]
    return digits


def split_mobile(phone: str) -> tuple[str, str]:
    digits = normalize_phone(phone)
    if len(digits) < 10:
        raise SystemExit(
            "Consignee phone must contain a full Israeli phone number for "
            "standard-shipment tests."
        )
    return digits[:3], digits[3:]


def resolve_pickup_point(client: ShipClient, config: Config, point_types: str):
    response = client.points.get_closest_points(
        city=config.consignee_city or config.city,
        street=config.consignee_street or config.street,
        house_number=config.consignee_house_number or config.house_number,
        point_types=point_types,
        points=1,
    )
    if not response.Points:
        raise SystemExit(f"No pickup point found for point type(s): {point_types}")
    return response.Points[0]


def confirm_real_api_call(config: Config) -> None:
    if not sys.stdin.isatty():
        raise SystemExit(
            "Interactive terminal confirmation is required for the real API call."
        )
    print(f"{COLOR_RED}WARNING: this will call the real SHIP API.{COLOR_RESET}")
    print(f"{COLOR_YELLOW}Review the target details before continuing:{COLOR_RESET}")
    print(
        f"{COLOR_CYAN}Point lookup:{COLOR_RESET} "
        f"{config.city}, {config.street} {config.house_number}"
    )
    if (
        config.run_insert_pickup_shipment
        or config.run_insert_pickup_drop_shipment
        or config.run_insert_standard_shipment
    ):
        print(
            f"{COLOR_CYAN}Shipment consignee:{COLOR_RESET} "
            f"{config.consignee_customer_name} / {config.consignee_phone}"
        )
    if config.run_insert_pickup_shipment or config.run_insert_pickup_drop_shipment:
        print(
            f"{COLOR_CYAN}Pickup point:{COLOR_RESET} "
            f"{config.pickup_point_type} / {config.pickup_point_id}"
        )
    answer = input("Type 'yes' to continue: ").strip().lower()
    if answer != "yes":
        raise SystemExit("Cancelled.")


def build_consignee(config: Config):
    return build_consignee_address(
        city_name=config.consignee_city or "",
        street_name=config.consignee_street or "",
        house_number=config.consignee_house_number or "",
        contact_person=config.consignee_contact_person or "",
        customer_name=config.consignee_customer_name or "",
        phone1=config.consignee_phone or "",
    )


def build_preparation(config: Config):
    return build_shipment_preparation(
        consignee_address=build_consignee(config),
        number_of_packages=config.number_of_packages,
        reference1=config.reference_1,
        reference2=config.reference_2,
        shipment_instructions=config.shipment_instructions,
        context_customer_id=int(config.customer_id),
    )


def build_standard_shipment(config: Config) -> StandardShipmentRequest:
    mobile_prefix, mobile = split_mobile(config.consignee_phone or "")
    return StandardShipmentRequest(
        Weight=config.standard_weight,
        ShipmentType=config.standard_shipment_type,
        Reference1=config.reference_1,
        Reference2=config.reference_2,
        NumberOfPackages=config.number_of_packages,
        NumberOfPackagesToReturn=config.standard_number_of_packages_to_return,
        ConsigneeAddress=build_standard_address(
            city_name=config.consignee_city or "",
            street_name=config.consignee_street or "",
            house_number=config.consignee_house_number or "",
            contact_person=config.consignee_contact_person or "",
            customer_name=config.consignee_customer_name or "",
            phone=mobile,
            phone_prefix=mobile_prefix,
            mobile=mobile,
            mobile_prefix=mobile_prefix,
        ),
        DDO=config.standard_ddo,
        IsReturn=config.standard_is_return,
        UDRValue=config.standard_udr_value,
        CODValue=config.standard_cod_value,
        Instruction=config.standard_instruction,
        UseDefaultShipperAddress=True,
        PickupPointID=config.standard_pickup_point_id,
    )


def build_pricing_payload(payload: Any | None):
    if payload is not None:
        return payload
    return PricingRequest(
        PackageType=2,
        IsExport=True,
        ShipmentValue=10,
        ToZipCode="10015",
        ToCountryCode="US",
        ToCity="New york",
        Packages=[PricingPackage(Length=0, Width=0, Height=0, Weight=10)],
    )


def main() -> None:
    config = load_config()
    if config.run_insert_pickup_shipment or config.run_insert_pickup_drop_shipment:
        require_pickup_shipment_config(config)
    if config.run_insert_standard_shipment:
        require_standard_shipment_config(config)
    confirm_real_api_call(config)

    environment = Environment.__members__[config.environment]
    client = ShipClient(
        username=config.username,
        password=config.password,
        customer_id=config.customer_id,
        environment=environment,
    )

    try:
        client.login()
        print("Authentication: ok")
        points = client.points.get_closest_points(
            city=config.city,
            street=config.street,
            house_number=config.house_number,
            point_types=config.point_types,
            points=config.points_limit,
        )
        print(f"Closest points: {len(points.Points)}")
        if points.Points:
            print(points.model_dump_json(indent=2))
    except AuthenticationError as exc:
        print(f"Authentication failed: {exc}")
        raise SystemExit(1) from exc
    except ShipAPIError as exc:
        print(f"API error: {exc}")
        raise SystemExit(1) from exc

    tracking_number = config.tracking_number
    pickup_point_id = config.pickup_point_id
    pickup_point_type = config.pickup_point_type
    pickup_drop_point_id = config.pickup_drop_point_id
    pickup_drop_point_type = config.pickup_drop_point_type

    if config.run_insert_pickup_shipment and (
        not pickup_point_id or not pickup_point_type
    ):
        nearest_pickup = resolve_pickup_point(client, config, "1")
        pickup_point_id = str(nearest_pickup.PointID)
        pickup_point_type = str(nearest_pickup.PointType)
        print(f"Resolved pickup point: {pickup_point_type} / {pickup_point_id}")

    if config.run_insert_pickup_drop_shipment and (
        not pickup_drop_point_id or not pickup_drop_point_type
    ):
        nearest_drop = resolve_pickup_point(client, config, "4")
        pickup_drop_point_id = str(nearest_drop.PointID)
        pickup_drop_point_type = str(nearest_drop.PointType)
        print(
            f"Resolved pickup-drop point: "
            f"{pickup_drop_point_type} / {pickup_drop_point_id}"
        )

    if config.run_insert_pickup_shipment:
        preparation = build_preparation(config)
        pickup_shipment = build_pickup_shipment_request(
            preparation=preparation,
            pickup_point_id=pickup_point_id or "",
            pickup_point_type=pickup_point_type or "",
        )
        response = client.shipments.insert_pickup_shipment(pickup_shipment)
        print("Pickup shipment response:")
        print(response.model_dump_json(indent=2))
        tracking_number = response.Result.TrackingNumber or tracking_number

    if config.run_insert_pickup_drop_shipment:
        preparation = build_preparation(config)
        pickup_drop_shipment = build_pickup_shipment_request(
            preparation=preparation,
            pickup_point_id=pickup_drop_point_id or "",
            pickup_point_type=pickup_drop_point_type or "",
        )
        response = client.shipments.insert_pickup_drop_shipment(pickup_drop_shipment)
        print("Pickup-drop shipment response:")
        print(response.model_dump_json(indent=2))
        tracking_number = response.Result.TrackingNumber or tracking_number

    if config.run_insert_standard_shipment:
        standard_shipment = build_standard_shipment(config)
        response = client.shipments.insert_standard_shipment(standard_shipment)
        print("Standard shipment response:")
        print(response.model_dump_json(indent=2))
        tracking_number = response.Result.TrackingNumber or tracking_number

    if config.run_insert_picking_list:
        payload = build_picking_list_payload(
            config.picking_list_payload,
            config.customer_id,
            config.reference_1,
            tracking_number,
        )
        response = client.shipments.insert_picking_list(payload)
        print("Picking list response:")
        print(response.model_dump_json(indent=2))

    if config.run_print_wb_order_details:
        params = build_tracking_params(
            "SHIP_PRINT_WB_ORDER_DETAILS_PARAMS_JSON",
            config.print_wb_order_details_params,
            tracking_number,
        )
        response = client.shipments.print_wb_order_details(**params)
        print("WB order details response:")
        print(
            json.dumps(
                {
                    "MediaType": response.MediaType,
                    "FileName": response.FileName,
                    "FileBytesLength": len(response.file_bytes()),
                },
                indent=2,
                ensure_ascii=False,
            )
        )

    if config.run_get_wb_status:
        params = build_tracking_params(
            "SHIP_WB_STATUS_PARAMS_JSON",
            config.wb_status_params,
            tracking_number,
        )
        response = client.shipments.get_wb_status(**params)
        print("WB status response:")
        print(response.model_dump_json(indent=2))

    if config.run_get_pricing:
        pricing = client.shipments.get_pricing(
            build_pricing_payload(config.pricing_payload)
        )
        print("Pricing response:")
        print(pricing.model_dump_json(indent=2))

    if config.run_download_label:
        if not tracking_number:
            raise SystemExit("No tracking number available for label download.")
        label = client.labels.download_label(
            tracking_number=tracking_number,
            label_format=config.label_format,
            copies=config.label_copies,
        )
        output = Path(config.label_output or label.FileName)
        output.write_bytes(label.file_bytes())
        print(f"Label written to: {output}")


if __name__ == "__main__":
    main()
