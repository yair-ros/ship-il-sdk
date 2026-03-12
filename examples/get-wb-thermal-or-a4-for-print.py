import os
from pathlib import Path

from ship_il_sdk import Environment, ShipClient


client = ShipClient(
    username=os.environ["SHIP_API_USER"],
    password=os.environ["SHIP_API_PASSWORD"],
    customer_id=os.environ["SHIP_CUSTOMER_ID"],
    environment=Environment[os.environ.get("SHIP_ENV", "DEV").upper()],
)

label = client.labels.download_label(
    tracking_number=os.environ["SHIP_TRACKING_NUMBER"],
    label_format=os.environ.get("SHIP_LABEL_FORMAT", "thermal"),
    copies=int(os.environ.get("SHIP_LABEL_COPIES", "3")),
)

output_path = Path(os.environ.get("SHIP_LABEL_OUTPUT", label.FileName))
output_path.write_bytes(label.file_bytes())

print(
    {
        "media_type": label.MediaType,
        "file_name": label.FileName,
        "written_to": str(output_path),
    }
)
