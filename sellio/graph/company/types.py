from pydantic import dataclasses


@dataclasses.dataclass(frozen=True)
class CompanyDeliveryOptionContext:
    id: int
    type: str
    name: str


@dataclasses.dataclass(frozen=True)
class CompanyPaymentOptionContext:
    id: int
    type: str
    name: str

