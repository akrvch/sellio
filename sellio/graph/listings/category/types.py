import dataclasses

from sellio.graph.listing_page.types import ListingPageContext


@dataclasses.dataclass(frozen=True)
class CategoryListingContext:
    category_id: int
    page: ListingPageContext | None
