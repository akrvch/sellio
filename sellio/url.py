from slugify import slugify


def category(category_alias: str, absolute: bool = False) -> str:
    path = f"/c/{category_alias}"
    if absolute:
        return f"http://localhost:5173{path}"
    return path


def product(id, product_name: str, absolute: bool = False) -> str:
    path = f"/p/{id}-{slug}"
    slug = slugify(product_name)
    if absolute:
        return f"http://localhost:5173{path}"
    return path