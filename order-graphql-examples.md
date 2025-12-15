# Order GraphQL API Examples

## Запити (Queries)

### 1. Checkout - отримати дані для сторінки оформлення замовлення

```graphql
query GetCheckout {
  checkout(cartId: 123) {
    cart {
      id
      totalAmount
      items {
        productId
        name
        price
        quantity
        product {
          id
          name
          description
        }
      }
      company {
        id
        name
        email
        phone
        paymentOptions {
          id
          name
          type
        }
        deliveryOptions {
          id
          name
          type
        }
      }
    }
  }
}
```

### 2. Thank You Page - отримати дані для сторінки подяки після замовлення

```graphql
query GetThankYouPage {
  thankYouPage(orderId: 456) {
    order {
      id
      fromFirstName
      fromSecondName
      fromLastName
      fromEmail
      fromPhone
      status {
        key
        title
      }
      comment
      dateCreated
      cart {
        id
        totalAmount
        items {
          name
          price
          quantity
        }
      }
      company {
        name
        phone
      }
      paymentOption {
        name
        type
      }
      deliveryOption {
        name
        type
      }
      deliveryInfo {
        id
        status {
          key
          title
        }
        declarationId
        city
        warehouse
        fullDeliveryAddress
      }
    }
  }
}
```

### 3. Order List - список замовлень користувача

```graphql
query GetOrderList {
  orderList(limit: 10, offset: 0) {
    id
    fromFirstName
    fromLastName
    status {
      key
      title
    }
    dateCreated
    cart {
      totalAmount
    }
    company {
      name
    }
  }
}
```

### 4. Order Details - деталі конкретного замовлення

```graphql
query GetOrderDetails {
  orderDetails(id: 123) {
    id
    fromFirstName
    fromSecondName
    fromLastName
    fromEmail
    fromPhone
    status {
      key
      title
    }
    comment
    dateCreated
    cart {
      id
      totalAmount
      items {
        name
        price
        quantity
      }
    }
    paymentOption {
      name
      type
    }
    deliveryOption {
      name
      type
    }
    deliveryInfo {
      id
      status {
        key
        title
      }
      declarationId
      city
      warehouse
      fullDeliveryAddress
    }
    company {
      name
      email
      phone
    }
  }
}
```

## Мутації (Mutations)

### Create Order - створення нового замовлення

```graphql
mutation CreateOrder {
  createOrder(
    cartId: 123
    paymentOptionId: 1
    deliveryOptionId: 2
    fromFirstName: "Іван"
    fromSecondName: "Петрович"
    fromLastName: "Сидоренко"
    fromPhone: "+380501234567"
    fromEmail: "ivan@example.com"
    comment: "Прошу зателефонувати перед доставкою"
    city: "Київ"
    warehouse: "Відділення №15"
    fullDeliveryAddress: "м. Київ, Відділення №15, вул. Хрещатик, 1"
  ) {
    success
    message
    orderId
  }
}
```

## Приклади використання

### Повнийflow створення замовлення:

1. **Додавання товарів до кошика:**
```graphql
mutation AddToCart {
  addItemToCart(productId: 10) {
    success
    message
    cart {
      id
      totalAmount
    }
  }
}
```

2. **Перехід на checkout:**
```graphql
query {
  checkout(cartId: 123) {
    cart { 
      id
      totalAmount
      company { 
        paymentOptions { id name type }
        deliveryOptions { id name type }
      }
    }
  }
}
```

3. **Створення замовлення:**
```graphql
mutation {
  createOrder(...) {
    success
    message
    orderId
  }
}
```

4. **Перехід на thank you page:**
```graphql
query {
  thankYouPage(orderId: 456) {
    order {
      id
      status { key title }
      dateCreated
      deliveryInfo {
        status { key title }
      }
    }
  }
}
```

## Приклади роботи зі статусами

### Відображення статусу замовлення:
```graphql
query {
  orderDetails(id: 123) {
    id
    status {
      key    # "new"
      title  # "Нове"
    }
  }
}
```

### Фільтрація по статусу (на frontend):
```javascript
// Приклад використання на фронтенді
const order = await fetchOrder(123);

if (order.status.key === "new") {
  // Замовлення нове, показати кнопку "Скасувати"
}

if (order.status.key === "completed") {
  // Замовлення виконано, показати кнопку "Залишити відгук"
}

// Відображення статусу користувачу
console.log(`Статус: ${order.status.title}`); // "Статус: Нове"
```

### Перевірка статусу доставки:
```graphql
query {
  orderDetails(id: 123) {
    deliveryInfo {
      id
      status {
        key    # "sent"
        title  # "Відправлено"
      }
      declarationId
    }
  }
}
```

## Типи

### OrderStatus
Тип статусу замовлення (об'єкт):
- `key` (String) - ключ статусу
- `title` (String) - назва статусу

**Можливі значення:**
| key | title |
|-----|-------|
| `new` | Нове |
| `in_progress` | Прийнято |
| `completed` | Виконано |
| `cancelled` | Скасовано |

### DeliveryInfoStatus
Тип статусу доставки (об'єкт):
- `key` (String) - ключ статусу
- `title` (String) - назва статусу

**Можливі значення:**
| key | title |
|-----|-------|
| `init` | Ініційовано |
| `created` | Створено |
| `sent` | Відправлено |
| `delivered` | Доставлено |
| `cancelled` | Скасовано |
| `completed` | Завершено |
| `returned` | Повернено |

### Order
Основні поля замовлення:
- `id` - ID замовлення
- `fromFirstName`, `fromSecondName`, `fromLastName` - ПІБ замовника
- `fromEmail`, `fromPhone` - контактні дані
- `status` - статус замовлення (об'єкт OrderStatus)
- `comment` - коментар до замовлення (optional)
- `dateCreated` - дата створення у форматі "YYYY-MM-DD HH:MM:SS"
- `cart` - кошик (лінка до Cart)
- `company` - компанія (лінка до Company)
- `paymentOption` - спосіб оплати (лінка до PaymentOption)
- `deliveryOption` - спосіб доставки (лінка до DeliveryOption)
- `deliveryInfo` - інформація про доставку (optional, лінка до DeliveryInfo)

### DeliveryInfo
Інформація про доставку:
- `id` - ID
- `status` - статус доставки (об'єкт DeliveryInfoStatus)
- `declarationId` - номер декларації (optional)
- `city` - місто (optional)
- `warehouse` - відділення (optional)
- `fullDeliveryAddress` - повна адреса доставки (optional)

## Важливі примітки

### Валідація при створенні замовлення:
- Користувач повинен бути автентифікованим
- Кошик повинен належати поточному користувачу
- `paymentOptionId` повинен належати компанії з кошика і бути активним
- `deliveryOptionId` повинен належати компанії з кошика і бути активним
- Якщо валідація не проходить, повертається `success: false` з відповідним повідомленням

### Поля CreateOrderResponse:
- `success` (Boolean) - чи успішно створено замовлення
- `message` (String) - повідомлення про результат операції
- `orderId` (Integer, nullable) - ID створеного замовлення (null якщо помилка)

### Формат дати:
- `dateCreated` - повертається у форматі `"YYYY-MM-DD HH:MM:SS"` (наприклад: "2025-12-14 15:30:45")

### Приклад відповіді зі статусом:
```json
{
  "status": {
    "key": "new",
    "title": "Нове"
  }
}
```

## Приклади відповідей API

### Успішне створення замовлення:
```json
{
  "data": {
    "createOrder": {
      "success": true,
      "message": "Order created successfully",
      "orderId": 456
    }
  }
}
```

### Помилка створення (невалідний способ оплати):
```json
{
  "data": {
    "createOrder": {
      "success": false,
      "message": "Invalid or inactive payment option for this company",
      "orderId": null
    }
  }
}
```

### Відповідь checkout:
```json
{
  "data": {
    "checkout": {
      "cart": {
        "id": 123,
        "totalAmount": "1250.50",
        "items": [
          {
            "productId": 10,
            "name": "Товар 1",
            "price": "500.00",
            "quantity": 2
          },
          {
            "productId": 15,
            "name": "Товар 2",
            "price": "250.50",
            "quantity": 1
          }
        ],
        "company": {
          "id": 1,
          "name": "Магазин XYZ",
          "paymentOptions": [
            {
              "id": 1,
              "name": "Готівка",
              "type": "cash"
            },
            {
              "id": 2,
              "name": "Карткою",
              "type": "card"
            }
          ],
          "deliveryOptions": [
            {
              "id": 1,
              "name": "Нова Пошта",
              "type": "nova_poshta"
            },
            {
              "id": 2,
              "name": "Самовивіз",
              "type": "pickup"
            }
          ]
        }
      }
    }
  }
}
```

### Відповідь orderDetails:
```json
{
  "data": {
    "orderDetails": {
      "id": 123,
      "fromFirstName": "Іван",
      "fromSecondName": "Петрович",
      "fromLastName": "Сидоренко",
      "fromEmail": "ivan@example.com",
      "fromPhone": "+380501234567",
      "status": {
        "key": "in_progress",
        "title": "Прийнято"
      },
      "comment": "Прошу зателефонувати перед доставкою",
      "dateCreated": "2025-12-14 15:30:45",
      "cart": {
        "id": 100,
        "totalAmount": "1250.50"
      },
      "deliveryInfo": {
        "id": 50,
        "status": {
          "key": "created",
          "title": "Створено"
        },
        "declarationId": "20450012345678",
        "city": "Київ",
        "warehouse": "Відділення №15",
        "fullDeliveryAddress": "м. Київ, Відділення №15, вул. Хрещатик, 1"
      },
      "company": {
        "name": "Магазин XYZ",
        "email": "info@xyz.com",
        "phone": "+380441234567"
      }
    }
  }
}
```

