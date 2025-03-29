import json
from pathlib import Path

import toml
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text


def get_db_url() -> str:
    config = toml.load(Path(__file__).parent.parent / "config/dev.toml")
    db_config = config["main_db"]
    user = db_config["user"]
    password = db_config["password"]
    host = db_config["host"]
    port = db_config["port"]
    db = db_config["db"]
    driver = "postgresql"
    return f"{driver}://{user}:{password}@{host}:{port}/{db}"


engine = create_engine(get_db_url(), echo=True)
metadata = MetaData()

category_table = Table("category", metadata, autoload_with=engine)
user_table = Table("user", metadata, autoload_with=engine)
company_table = Table("company", metadata, autoload_with=engine)
delivery_option_table = Table("delivery_option", metadata, autoload_with=engine)
payment_option_table = Table("payment_option", metadata, autoload_with=engine)
product_table = Table("product", metadata, autoload_with=engine)


def insert_categories(connection) -> None:
    with open(Path(__file__).parent / "categories-mocks.json") as f:
        categories = json.load(f)

    connection.execute(sa_text("TRUNCATE category CASCADE"))
    connection.execute(category_table.insert(), categories)


def insert_users(connection) -> None:
    with open(Path(__file__).parent / "users-mocks.json") as f:
        users = json.load(f)

    connection.execute(sa_text('TRUNCATE "user" CASCADE'))
    connection.execute(user_table.insert(), users)


def insert_companies(connection) -> None:
    with open(Path(__file__).parent / "companies-mocks.json") as f:
        companies = json.load(f)

    connection.execute(sa_text("TRUNCATE company CASCADE"))
    connection.execute(company_table.insert(), companies)


def insert_deliveries(connection) -> None:
    with open(Path(__file__).parent / "deliveries-mocks.json") as f:
        deliveries = json.load(f)

    connection.execute(sa_text("TRUNCATE delivery_option CASCADE"))
    connection.execute(delivery_option_table.insert(), deliveries)


def insert_payments(connection) -> None:
    with open(Path(__file__).parent / "payments-mocks.json") as f:
        payments = json.load(f)

    connection.execute(sa_text("TRUNCATE payment_option CASCADE"))
    connection.execute(payment_option_table.insert(), payments)


def insert_products(connection) -> None:
    with open(Path(__file__).parent / "products-mocks.json") as f:
        products = json.load(f)

    connection.execute(sa_text("TRUNCATE product CASCADE"))
    connection.execute(product_table.insert(), products)


if __name__ == "__main__":
    with engine.begin() as conn:
        insert_categories(conn)
        insert_users(conn)
        insert_companies(conn)
        insert_deliveries(conn)
        insert_payments(conn)
        insert_products(conn)
