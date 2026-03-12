from .specs import DOWNLOAD_LABEL


class LabelsAPI:
    def __init__(self, client):
        self.client = client

    def download_label(self, tracking_number, label_format="thermal", copies=3):
        return self.client._request_model(
            DOWNLOAD_LABEL,
            params={
                "trackingNumber": tracking_number,
                "labelFormat": label_format,
                "copies": copies,
            },
        )
