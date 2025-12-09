from sellio.lib.slugify import slugify


def category(category_alias: str, absolute: bool = False) -> str:
    path = f"/c/{category_alias}"
    if absolute:
        return f"http://localhost:5173{path}"
    return path


def product(id, product_name: str, absolute: bool = False) -> str:
    slug = slugify(product_name)
    path = f"/p/{id}-{slug}"
    if absolute:
        return f"http://localhost:5173{path}"
    return path
