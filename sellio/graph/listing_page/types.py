import dataclasses


@dataclasses.dataclass(frozen=True)
class ListingPageContext:
    product_ids: tuple[int, ...]
