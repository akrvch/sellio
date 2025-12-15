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

**Базовий запуск (тільки backend):**
```sh
lets run
```
### Або за допомогою docker compose
```sh
docker compose up postgres sellio nginx
```


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

## Cart Service Integration

Проект інтегрований з окремим мікросервісом кошика (sellio-cart). Всі запити до кошика проксуються через GraphQL API.

### Налаштування

Переконайтеся, що в `config/dev.toml` вказано URL сервісу кошика:

```toml
cart_service_url = 'http://sellio-cart:8080'
```

### Приклад роботи з кошиком

Отримати кошики поточного користувача:

```graphql
query {
  userCarts {
    id
    companyId
    items {
      productId
      name
      quantity
      price
      product {
        name
        discountedPrice
      }
    }
    totalAmount
  }
}
```

Додати товар у кошик (дані про товар беруться з бази автоматично, кошик створюється при потребі):

```graphql
mutation {
  addItemToCart(
    companyId: 100
    productId: 501
  ) {
    success
    message
    cart {
      id
      items {
        productId
        quantity
      }
      totalAmount
    }
  }
}
```

Оновити кількість товару:

```graphql
mutation {
  updateCartItemQuantity(
    companyId: 100
    productId: 501
    quantity: 5
  ) {
    success
    message
  }
}
```

Видалити товар з кошика:

```graphql
mutation {
  removeItemFromCart(
    companyId: 100
    productId: 501
  ) {
    success
    message
  }
}
```

**Документація:**
- Короткий огляд: [sellio/graph/cart/README.md](sellio/graph/cart/README.md)
- Детальна документація з прикладами: [sellio/graph/cart/CART_API.md](sellio/graph/cart/CART_API.md)

