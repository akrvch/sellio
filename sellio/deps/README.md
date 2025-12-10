# Global Request Context

Цей модуль надає глобальний доступ до поточного HTTP request через `contextvars`.

## Як це працює

### 1. Middleware встановлює контекст

`RequestContextMiddleware` в `main.py` автоматично:
- Встановлює поточний `request` в contextvars на початку кожного запиту
- Ініціалізує список для pending cookies
- Після обробки запиту додає всі pending cookies до response

### 2. Використання в коді

```python
from sellio.deps.request import get_cookie, set_cookie

# В будь-якому resolver або функції під час обробки запиту:

# Прочитати cookie
auth_token = get_cookie("sellio_auth_token")

# Встановити cookie (буде додано до response автоматично)
set_cookie(
    key="sellio_auth_token",
    value="token_value",
    httponly=True,
    secure=False,
    samesite="lax",
    max_age=60 * 60 * 24 * 30,  # 30 days
)
```

### 3. Автоматична інтеграція з GraphQL

`get_graph_context()` автоматично додає auth token з cookies до GraphQL контексту:

```python
context = {
    "db.session_async": main_db,
    "auth.token": "<значення з cookie>",  # додається автоматично
}
```

## Переваги

1. **Чистота коду** - endpoint залишається простим, без логіки обробки cookies
2. **Інкапсуляція** - resolvers самі керують своїми cookies
3. **Безпека** - HTTPOnly cookies недоступні для JavaScript
4. **Зручність** - не потрібно передавати request/response через параметри

## Приклад використання

```python
# sellio/graph/auth/resolvers.py

from sellio.deps.request import set_cookie

@pass_context
async def mutation_verify_auth_code(ctx, opts):
    # ... verify code logic ...
    
    # Встановити auth cookie
    set_cookie(
        key=AUTH_COOKIE_NAME,
        value=session_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )
    
    return [{"status": "SUCCESS", ...}]
```

Cookie буде автоматично додано до HTTP response middleware'ом.

