import json
from pathlib import Path

from sqlalchemy import create_engine, MetaData, Table
import toml

def get_db_url() -> str:
    config = toml.load(Path(__file__).parent.parent / "config/dev.toml")
    db_config = config["main_db"]
    user = db_config["user"]
    password = db_config["password"]
    host = db_config["host"]
    port = db_config["port"]
    db = db_config["db"]
    driver = "postgresql"
    print("FUCK")
    print(f"{driver}://{user}:{password}@{host}:{port}/{db}")
    return f"{driver}://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(get_db_url(), echo=True)
metadata = MetaData()

category_table = Table("category", metadata, autoload_with=engine)


def insert_categories(connection) -> None:
    with open(Path(__file__).parent / "categories-mocks.json") as f:
        categories = json.load(f)

    connection.execute(category_table.insert(), categories)


if __name__ == "__main__":
    with engine.begin() as conn:
        insert_categories(conn)