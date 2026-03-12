from .specs import GET_CLOSEST_POINTS


class PointsAPI:
    def __init__(self, client):
        self.client = client

    def get_closest_points(
        self,
        city,
        street,
        house_number,
        point_types="1,2,4",
        points=10,
    ):
        return self.client._request_model(
            GET_CLOSEST_POINTS,
            params={
                "city": city,
                "street": street,
                "houseNumber": house_number,
                "pointTypes": point_types,
                "points": points,
            },
        )
