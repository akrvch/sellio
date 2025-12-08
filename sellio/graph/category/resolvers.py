from typing import Any

from hiku.graph import Field
from hiku.graph import Nothing
from hiku.graph import NothingType

from sellio import url
from sellio.services.categories import CachedCategory
from sellio.services.categories import cached_categories


def map_categories(
    fields: list[Field], category_ids: list[int]
) -> list[list[CachedCategory]]:
    def get_field(category_id: int, field_name: str) -> Any:
        if not (category := cached_categories.get_category_by_id(category_id)):
            raise ValueError(f"Category with id {category_id} not found")

        match field_name:
            case "id":
                return category.id
            case "name":
                return category.name
            case "url":
                return url.category(category.alias, absolute=True)
            case "alias":
                return category.alias
            case "description":
                return category.description
            case "is_adult":
                return category.is_adult
            case "_path":
                return [
                    cat.id for cat in cached_categories.get_path(category_id)
                ]
            case "_child_categories":
                return [
                    cat.id
                    for cat in cached_categories.get_children(category_id)
                ]
        raise ValueError(f"Unknown field: '{field_name}'")

    return [
        [get_field(category_id, field.name) for field in fields]
        for category_id in category_ids
    ]


def link_category(opts: dict[str, str]) -> list[int] | NothingType:
    if not (alias := opts.get("alias")):
        return Nothing

    if not (category := cached_categories.get_category_by_alias(alias)):
        return Nothing

    return [category.id]
