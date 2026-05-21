from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class BookingDateOption(BaseModel):
    Id: str
    Title: str


class PickupDatesResponse(BaseModel):
    Dates: List[BookingDateOption] = Field(default_factory=list)
    ErrorMessage: Optional[str] = None


class PickupTimeOption(BaseModel):
    FromTime: str
    ToTime: str
    ServiceType: int
    Free: bool
    SelectedDay: Optional[str] = None


class BookingAddress(BaseModel):
    CustomerID: Optional[int] = None
    CustomerName: str
    CityName: str
    CityCode: Optional[int] = None
    CityCodeMapa: Optional[str] = None
    ContactPerson: str
    StreetCode: Optional[str] = None
    StreetCodeMapa: Optional[str] = None
    StreetName: str
    Phone: str
    PhonePrefix: str
    Mobile: str
    MobilePrefix: str
    LocationDescription: Optional[str] = None
    Story: Optional[str] = None
    HouseNumber: str
    Floor: Optional[str] = None
    RoomNumber: Optional[str] = None
    ContactEmail: Optional[str] = None
    Area: Optional[str] = None
    AreaCode: Optional[str] = None
    IsAccessPoint: Optional[bool] = None
    IsResidential: Optional[bool] = None
    Index: Optional[int] = None
    ZipCode: Optional[str] = None
    Tel: Optional[str] = None
    Tel2: Optional[str] = None


class BookingCustomerInfo(BaseModel):
    Address: BookingAddress
    CustomerID: Optional[int] = None
    CreditExportExpress: Optional[float] = None
    CreditDomestic: Optional[float] = None


class BookingRequest(BaseModel):
    UserOwnerAccount: Optional[str] = None
    Email: Optional[str] = None
    ContactPerson: str
    OpenBy: str
    Weight: float
    ServiceNumber: int
    PackagesNumber: float
    IsFlatPlace: bool
    ConfirmByMail: bool
    PickupToTime: str
    PickupFromTime: str
    PickupDate: str
    CustomerInfo: BookingCustomerInfo
    PackageType: int


class ExportBookingResponse(BaseModel):
    BookingNumber: Optional[str] = None
    Error: Optional[str] = None


class CancelBookingRequest(BaseModel):
    BookingNumber: int
    Reason: str


class CancelBookingResponse(BaseModel):
    IsSuccess: bool
    ErrorMessage: Optional[str] = None
    Error: Optional[str] = None

    @field_validator("IsSuccess", mode="before")
    @classmethod
    def parse_success_string(cls, value):
        if isinstance(value, str):
            return value.strip().lower() == "true"
        return value
