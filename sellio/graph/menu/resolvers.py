from sellio.services.categories import cached_categories

ROOT_CATEGORY_ID = 0


def link_menu() -> list[int]:
    if not (
        menu_top_categories := cached_categories.get_children(ROOT_CATEGORY_ID)
    ):
        raise RuntimeError("Root category not found")

    return (cat.id for cat in menu_top_categories)
