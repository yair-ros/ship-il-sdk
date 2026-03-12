from typing import List, Optional, Union

from pydantic import BaseModel


class PickupPoint(BaseModel):
    CityName: str
    Description: Optional[str] = None
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None
    PointID: Union[str, int]
    PointType: Union[str, int]
    PointNumber: Optional[Union[str, int]] = None
    Distance: Optional[float] = None
    Phone: Optional[str] = None
    PointName: Optional[str] = None
    StreetName: Optional[str] = None
    HouseNumber: Optional[Union[str, int]] = None


class ClosestPointsResponse(BaseModel):
    IsSuccessful: bool
    ResponseCode: Optional[str] = None
    HomeDelivery: Optional[int] = None
    ErrorMSG: Optional[str] = None
    Points: List[PickupPoint]
