# Session API

Простий API для роботи з користувацькими сесіями через cookies.

## Функції

### `login(user: User) -> None`

Логінить користувача, створюючи сесію та встановлюючи auth cookie.

**Параметри:**
- `user: User` - об'єкт користувача для логіну

**Що робить:**
1. Генерує session token
2. Створює запис в таблиці `auth_session`
3. Встановлює HTTPOnly cookie `sellio_auth` (термін дії: 30 днів)

**Приклад використання:**

```python
from sellio.services.session import login
from sellio.models.user import User

@pass_context
async def mutation_login(ctx: TGraphContext, opts: dict) -> list[dict]:
    # ... логіка верифікації ...
    
    # Логінимо користувача
    await login(user)
    
    return [{"status": "SUCCESS"}]
```

---

### `logout() -> None`

Розлогінює поточного користувача.

**Що робить:**
1. Читає session token з cookie
2. Інвалідує сесію в БД (встановлює `expires_at` на поточний час)
3. Видаляє cookie (встановлює `max_age=0`)

**Приклад використання:**

```python
from sellio.services.session import logout

@pass_context
async def mutation_logout(ctx: TGraphContext, opts: dict) -> list[dict]:
    await logout()
    return [{"status": "SUCCESS", "message": "Logged out"}]
```

---

### `get_current_user() -> User | None`

Повертає поточного авторизованого користувача або `None`.

**Що робить:**
1. Читає session token з cookie `sellio_auth`
2. Шукає активну сесію в БД
3. Перевіряє що сесія не прострочена
4. Повертає об'єкт користувача

**Приклад використання:**

```python
from sellio.services.session import get_current_user

@pass_context
async def mutation_update_profile(ctx: TGraphContext, opts: dict) -> list[dict]:
    user = await get_current_user()
    
    if not user:
        return [{"status": "ERROR", "message": "Not authenticated"}]
    
    # ... оновлення профілю ...
    
    return [{"status": "SUCCESS"}]
```

---

## Глобальний доступ

Всі ці функції використовують **глобальний доступ** через `contextvars`:

- ✅ Не потрібно передавати `request`/`response`
- ✅ Не потрібно передавати `session` бази даних
- ✅ Працює з будь-якого місця в коді під час обробки запиту
- ✅ Потокобезпечно завдяки `contextvars`

## Внутрішня реалізація

```python
# Використовує глобальні функції з sellio.deps.request:
from sellio.deps.request import get_cookie, set_cookie

# Використовує глобальний main_db:
from sellio.services.db import main_db
```

## Cookie деталі

**Назва:** `sellio_auth`  
**Тип:** HTTPOnly (недоступна для JavaScript)  
**SameSite:** `lax`  
**Secure:** `False` (встановити `True` на production з HTTPS)  
**Термін дії:** 30 днів

## Приклад повного флоу

```python
from sellio.services.session import login, logout, get_current_user

# 1. Логін після верифікації OTP
async def verify_otp(phone, code):
    # ... verify code ...
    await login(user)  # Автоматично встановлює cookie

# 2. Доступ до поточного користувача
async def get_profile():
    user = await get_current_user()
    if not user:
        return {"error": "Not authenticated"}
    return {"name": user.first_name}

# 3. Логаут
async def logout_user():
    await logout()  # Видаляє cookie та інвалідує сесію
```

