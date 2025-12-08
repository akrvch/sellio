import logging
from dataclasses import dataclass
from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sellio import GlobalProxy
from sellio import global_storage
from sellio.models.category import Category
from sellio.services.db import main_db

log = logging.getLogger(__name__)

_KEY = "categories.cached"


@dataclass(frozen=True)
class CachedCategory:
    id: int
    name: str
    alias: str
    description: str
    parent_category_id: int | None
    is_adult: bool


class CachedCategories:
    def __init__(self):
        self._categories_by_id: dict[int, CachedCategory] = {}
        self._categories_by_alias: dict[str, CachedCategory] = {}
        self._children_by_parent_id: dict[int | None, list[CachedCategory]] = {}

    async def load(self, session: "AsyncSession") -> None:
        log.info("Loading categories into cache...")

        result = await session.execute(select(Category))
        db_categories = result.scalars().all()

        categories = [
            CachedCategory(
                id=cat.id,
                name=cat.name,
                alias=cat.alias,
                description=cat.description,
                parent_category_id=cat.parent_category_id,
                is_adult=cat.is_adult,
            )
            for cat in db_categories
        ]

        for category in categories:
            self._categories_by_alias[category.alias] = category
            self._categories_by_id[category.id] = category

        self._children_by_parent_id = {}
        for category in categories:
            parent_id = category.parent_category_id
            if parent_id not in self._children_by_parent_id:
                self._children_by_parent_id[parent_id] = []
            self._children_by_parent_id[parent_id].append(category)

        log.info(f"Loaded {len(categories)} categories into cache")

    def get_path(self, category_id: int) -> list[CachedCategory]:
        category = self.get_category_by_id(category_id)
        if category is None:
            return []

        path = [category]
        current_id = category_id

        while True:
            parent = self.get_parent(current_id)
            if parent is None:
                break
            path.insert(0, parent)
            current_id = parent.id

        return path

    def get_children(self, category_id: int | None) -> list[CachedCategory]:
        return self._children_by_parent_id.get(category_id, []).copy()

    def get_parent(self, category_id: int) -> CachedCategory | None:
        category = self._categories_by_id.get(category_id)
        if category is None:
            return None
        if category.parent_category_id is None:
            return None
        return self._categories_by_id.get(category.parent_category_id)

    def get_category_by_id(self, category_id: int) -> CachedCategory | None:
        return self._categories_by_id.get(category_id)

    def get_category_by_alias(
        self, category_alias: str
    ) -> CachedCategory | None:
        return self._categories_by_alias.get(category_alias)


cached_categories: "CachedCategories" = cast(
    CachedCategories, GlobalProxy(_KEY)
)

__all__ = [
    "CachedCategory",
    "cached_categories",
    "init_cached_categories",
]


async def init_cached_categories() -> None:
    cached = CachedCategories()
    async with main_db.session() as session:
        await cached.load(session)
    global_storage.set(_KEY, cached)
    log.info("Cached categories successfully initialized")
