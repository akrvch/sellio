from slugify import slugify as slugify_lib

def slugify(text: str) -> str:
    slug = slugify_lib(text)
    parts = slug.split("-")
    return "-".join(filter(lambda part: len(part) > 2 , parts))