import base64
from typing import List, Optional

from pydantic import BaseModel, Field


class ShipAddressInputModel(BaseModel):
    CityName: str
    StreetName: str
    HouseNumber: str
    ContactPerson: str
    CustomerName: str
    Phone1: str
    CityCode: Optional[int] = None
    StreetCode: Optional[int] = None
    LocationDescription: Optional[str] = None
    Phone2: Optional[str] = None
    RoomNumber: Optional[str] = None
    Floor: Optional[str] = None
    ZipCode: Optional[str] = None


class ShipmentRequest(BaseModel):
    ConsigneeAddress: ShipAddressInputModel
    ShipperAddress: Optional[ShipAddressInputModel] = None
    Reference1: Optional[str] = None
    Reference2: Optional[str] = None
    ShipmentInstructions: Optional[str] = None
    UseDefaultShipperAddress: bool = True
    NumberOfPackages: int
    PickupPointType: str
    PickupPointID: str
    ContextCustomerID: Optional[int] = None
    ContextUserEmail: Optional[str] = None
    UserDisplayName: Optional[str] = None
    OriginalData: Optional[str] = None


class ShipmentPreparationInput(BaseModel):
    ConsigneeAddress: ShipAddressInputModel
    ShipperAddress: Optional[ShipAddressInputModel] = None
    Reference1: Optional[str] = None
    Reference2: Optional[str] = None
    ShipmentInstructions: Optional[str] = None
    UseDefaultShipperAddress: bool = True
    NumberOfPackages: int
    ContextCustomerID: Optional[int] = None
    ContextUserEmail: Optional[str] = None
    UserDisplayName: Optional[str] = None
    OriginalData: Optional[str] = None


class ShipmentResult(BaseModel):
    PackageTrackingNumbers: List[str] = Field(default_factory=list)
    ReturnPackageTrackingNumbers: List[str] = Field(default_factory=list)
    ReturnTrackingNumber: Optional[str] = None
    TrackingNumber: Optional[str] = None
    ErrorCode: int = 0
    ErrorMessage: str = ""


class WbShipmentInfoReducedModel(BaseModel):
    ConsigneeCityName: Optional[str] = None
    ConsigneeStreetName: Optional[str] = None
    ConsigneeCityNameEng: Optional[str] = None
    ConsigneeStreetNameEng: Optional[str] = None
    ConsigneeHouseNumber: Optional[str] = None
    ConsigneeRoomNumber: Optional[str] = None
    ConsigneeFloorNumber: Optional[str] = None
    RouteCode: Optional[str] = None


class WbShipmentReducedResultModel(BaseModel):
    Result: List[WbShipmentInfoReducedModel]


class ShipmentResponse(BaseModel):
    Result: ShipmentResult
    WbResult: Optional[WbShipmentReducedResultModel] = None


class LabelResponse(BaseModel):
    MediaType: str
    FileByteArray: str
    FileName: str

    def file_bytes(self) -> bytes:
        return base64.b64decode(self.FileByteArray)
