from dataclasses import dataclass
from typing import Generic, Type, TypeVar

ResponseT = TypeVar("ResponseT")


@dataclass(frozen=True)
class EndpointSpec(Generic[ResponseT]):
    name: str
    method: str
    path: str
    response_model: Type[ResponseT]
