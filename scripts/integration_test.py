from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from ship_il_sdk import (
    Environment,
    ShipClient,
    build_consignee_address,
    build_pickup_shipment_request,
    build_shipment_preparation,
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
    run_create_shipment: bool
    consignee_city: str | None
    consignee_street: str | None
    consignee_house_number: str | None
    consignee_contact_person: str | None
    consignee_customer_name: str | None
    consignee_phone: str | None
    pickup_point_type: str | None
    pickup_point_id: str | None
    reference_1: str | None
    reference_2: str | None
    shipment_instructions: str | None
    number_of_packages: int
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
        points_limit=int(values.get("SHIP_POINTS_LIMIT", "10").strip()),
        run_create_shipment=bool_value(values, "SHIP_RUN_CREATE_SHIPMENT"),
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
        reference_1=optional_value(values, "SHIP_REFERENCE_1"),
        reference_2=optional_value(values, "SHIP_REFERENCE_2"),
        shipment_instructions=optional_value(values, "SHIP_SHIPMENT_INSTRUCTIONS"),
        number_of_packages=int(values.get("SHIP_NUMBER_OF_PACKAGES", "1").strip()),
        run_download_label=bool_value(values, "SHIP_RUN_DOWNLOAD_LABEL"),
        tracking_number=optional_value(values, "SHIP_TRACKING_NUMBER"),
        label_format=values.get("SHIP_LABEL_FORMAT", "thermal").strip(),
        label_copies=int(values.get("SHIP_LABEL_COPIES", "1").strip()),
        label_output=optional_value(values, "SHIP_LABEL_OUTPUT"),
    )


def require_shipment_config(config: Config) -> None:
    required = {
        "SHIP_CONSIGNEE_CITY": config.consignee_city,
        "SHIP_CONSIGNEE_STREET": config.consignee_street,
        "SHIP_CONSIGNEE_HOUSE_NUMBER": config.consignee_house_number,
        "SHIP_CONSIGNEE_CONTACT_PERSON": config.consignee_contact_person,
        "SHIP_CONSIGNEE_CUSTOMER_NAME": config.consignee_customer_name,
        "SHIP_CONSIGNEE_PHONE": config.consignee_phone,
        "SHIP_PICKUP_POINT_TYPE": config.pickup_point_type,
        "SHIP_PICKUP_POINT_ID": config.pickup_point_id,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise SystemExit(
            f"Missing required shipment values in {ENV_FILE.name}: {', '.join(missing)}"
        )


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
    if config.run_create_shipment:
        print(
            f"{COLOR_CYAN}Shipment consignee:{COLOR_RESET} "
            f"{config.consignee_customer_name} / {config.consignee_phone}"
        )
        print(
            f"{COLOR_CYAN}Pickup point:{COLOR_RESET} "
            f"{config.pickup_point_type} / {config.pickup_point_id}"
        )
    answer = input("Type 'yes' to continue: ").strip().lower()
    if answer != "yes":
        raise SystemExit("Cancelled.")


def main() -> None:
    config = load_config()
    if config.run_create_shipment:
        require_shipment_config(config)
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

    if config.run_create_shipment:
        consignee = build_consignee_address(
            city_name=config.consignee_city or "",
            street_name=config.consignee_street or "",
            house_number=config.consignee_house_number or "",
            contact_person=config.consignee_contact_person or "",
            customer_name=config.consignee_customer_name or "",
            phone1=config.consignee_phone or "",
        )
        preparation = build_shipment_preparation(
            consignee_address=consignee,
            number_of_packages=config.number_of_packages,
            reference1=config.reference_1,
            reference2=config.reference_2,
            shipment_instructions=config.shipment_instructions,
            context_customer_id=int(config.customer_id),
        )
        shipment = build_pickup_shipment_request(
            preparation=preparation,
            pickup_point_id=config.pickup_point_id or "",
            pickup_point_type=config.pickup_point_type or "",
        )
        response = client.shipments.insert_pickup_shipment(shipment)
        print("Shipment creation response:")
        print(response.model_dump_json(indent=2))
        tracking_number = response.Result.TrackingNumber or tracking_number

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
