# Sellio

## Що потрібно для запуску і розробки?

* [Docker](https://docs.docker.com/engine/install/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [uv](https://docs.astral.sh/uv/getting-started/installation/) для керування віртуальним середовищем та залежностями.
* [lets-cli](https://lets-cli.org/docs/installation) (опційно) для зручних команд для запуску проекту.

## Налаштування віртуального середовища
Проект використовує uv як менеджер пакетів.

### Створення віртуального середовища:
```sh
uv venv .venv             # створення
source .venv/bin/activate # запуск
uv sync --frozen          # встановлення залежностей
```
## Локальний запуск проекта

### Наповнення БД тестовимими даними
Піднімаємо базу
```sh
docker compose up postgres
```
Тепер потрібно застосувати міграції (створити таблиці в базі):
```sh
uv run alembic upgrade head
```
Тепер база готова для того, щоб її можна було заповнити тестовими даними:
```sh
uv run scripts/fill_db_with_mock_info.py
```

Далі можна перейти до запуску проекту:
### За допомогою lets-cli

```sh
lets run
```
### Або за допомогою docker compose
```sh
docker compose up postgres sellio
```
Тепер бекенд буде доступний на http://localhost:8080/

GraphQL playground http://localhost:8080/graphqil

Приклад запиту на graphql:
```
query GetProducts($productIds: [Int!]!) {
  productList(productIds: $productIds){
    id
    name
    price
    companyId
    company {
      id
      name
      phone
      email
    }
    deliveryOptions {
      id
      name
      type
    }
    paymentOptions {
      id
      name
      type
    }
  }
}
```
Змінні:
```
{
  "productIds": [5, 4, 3, 2, 1, 10]
}
```

