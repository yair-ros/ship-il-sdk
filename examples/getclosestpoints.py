import os

from ship_il_sdk import Environment, ShipClient


client = ShipClient(
    username=os.environ["SHIP_API_USER"],
    password=os.environ["SHIP_API_PASSWORD"],
    customer_id=os.environ["SHIP_CUSTOMER_ID"],
    environment=Environment[os.environ.get("SHIP_ENV", "DEV").upper()],
)

points = client.points.get_closest_points(
    os.environ.get("SHIP_CITY", "Tel Aviv"),
    os.environ.get("SHIP_STREET", "Herzl"),
    os.environ.get("SHIP_HOUSE_NUMBER", "10"),
    point_types=os.environ.get("SHIP_POINT_TYPES", "1,2,4"),
    points=int(os.environ.get("SHIP_POINTS_LIMIT", "10")),
)

print(points.model_dump_json(indent=2))
