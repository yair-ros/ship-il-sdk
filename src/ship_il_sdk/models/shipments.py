import base64
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


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


class StandardAddressInputModel(BaseModel):
    CustomerName: str
    CityName: Optional[str] = None
    CityCode: Optional[int] = None
    ContactPerson: str
    StreetCode: Optional[int] = None
    StreetName: str
    Phone: str
    PhonePrefix: str
    Mobile: str
    MobilePrefix: str
    LocationDescription: Optional[str] = None
    HouseNumber: str
    Floor: Optional[str] = None
    RoomNumber: Optional[str] = None
    ContactEmail: Optional[str] = None
    ZipCode: Optional[str] = None
    Tel: Optional[str] = None
    Tel2: Optional[str] = None


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
    UseDefaultDestinationAddress: Optional[bool] = None


class StandardShipmentRequest(BaseModel):
    Weight: float
    ShipmentType: int = 0
    Reference2: Optional[str] = None
    Reference1: Optional[str] = None
    NumberOfPackages: int
    NumberOfPackagesToReturn: int = 0
    ConsigneeAddress: StandardAddressInputModel
    ShipperAddress: Optional[StandardAddressInputModel] = None
    DDO: bool = False
    IsReturn: bool = False
    UDRValue: Optional[int] = None
    CODValue: Optional[float] = None
    Instruction: Optional[str] = None
    UseDefaultShipperAddress: bool = True
    PickupPointID: Optional[str] = None


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

    @field_validator("ReturnTrackingNumber", "TrackingNumber", mode="before")
    @classmethod
    def empty_list_to_none(cls, value):
        if value == []:
            return None
        return value


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


class PickingListItem(BaseModel):
    SKU1: str
    Description: str
    Quantity: float
    Location: Optional[str] = None
    SKU2: Optional[str] = None
    WH: Optional[str] = None
    Remarks: Optional[str] = None


class PickingListRequest(BaseModel):
    Items: List[PickingListItem]
    CustomerNumber: Optional[int] = None
    Ref1: Optional[str] = None
    TrackNO: Optional[str] = None


class PickingListResponse(BaseModel):
    ReturnValue: Optional[int] = None
    ErrorDescription: Optional[str] = None
    ErrorCode: Optional[int] = None


class FileResponse(BaseModel):
    MediaType: str
    FileByteArray: str
    FileName: Optional[str] = None

    def file_bytes(self) -> bytes:
        return base64.b64decode(self.FileByteArray)


class ShipmentProgressActivity(BaseModel):
    Activity: Optional[str] = None
    LocalTime: Optional[str] = None
    LocalDate: Optional[str] = None
    Location: Optional[str] = None


class WbStatusResponse(BaseModel):
    Status: Optional[str] = None
    DeliveredOn: Optional[str] = None
    LeftAt: Optional[str] = None
    RecivedBy: Optional[str] = None
    Receipent: Optional[str] = None
    Weight: Optional[str] = None
    Dispatch: Optional[str] = None
    LastSite: Optional[str] = None
    Service: Optional[str] = None
    ShipmentProgress: List[ShipmentProgressActivity] = Field(default_factory=list)

    @field_validator("ShipmentProgress", mode="before")
    @classmethod
    def none_progress_to_list(cls, value):
        if value is None:
            return []
        return value


class PricingItem(BaseModel):
    Fee: Optional[str] = None
    FeeCode: Optional[str] = None
    Price: Optional[float] = None
    RowType: Optional[int] = None


class PricingOption(BaseModel):
    Items: List[PricingItem] = Field(default_factory=list)
    ServiceCode: Optional[int] = None
    SeviceName: Optional[str] = None
    Days: Optional[int] = None
    EstimatedDate: Optional[str] = None


class PricingPackage(BaseModel):
    Height: int = 0
    Length: int = 0
    Width: int = 0
    Weight: float


class PricingRequest(BaseModel):
    ToCountryCode: str
    IsExport: bool
    PackageType: int
    ShipmentValue: float
    ToZipCode: str
    ToCity: str
    Packages: List[PricingPackage]
    FromPostcode: Optional[str] = None
    PickupDate: Optional[str] = None


class PricingResponse(BaseModel):
    ServicesPricing: List[PricingOption] = Field(default_factory=list)


class LabelResponse(FileResponse):
    FileName: str
