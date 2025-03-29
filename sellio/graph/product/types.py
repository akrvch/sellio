from pydantic import dataclasses


@dataclasses.dataclass(frozen=True)
class ProductDeliveryOptionContext:
    id: int
    type: str
    name: str


@dataclasses.dataclass(frozen=True)
class ProductPaymentOptionContext:
    id: int
    type: str
    name: str
