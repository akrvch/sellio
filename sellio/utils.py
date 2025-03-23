DB_DRIVER_NAME = "asyncpg"


def get_sql_alchemy_db_url(
    user: str,
    password: str,
    host: str,
    port: str,
    db: str,
) -> str:
    driver = "+".join(("postgresql", DB_DRIVER_NAME))
    return f"{driver}://{user}:{password}@{host}:{port}/{db}"
