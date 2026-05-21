from dataclasses import dataclass
from typing import Generic, Optional, Type, TypeVar

ResponseT = TypeVar("ResponseT")


@dataclass(frozen=True)
class EndpointSpec(Generic[ResponseT]):
    name: str
    method: str
    path: str
    response_model: Optional[Type[ResponseT]]
