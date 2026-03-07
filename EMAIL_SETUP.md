# 📧 Настройка Email-уведомлений на Railway

## 📊 Текущее состояние
❌ Email-уведомления **ОТКЛЮЧЕНЫ** (письма записываются только в логи Railway)

---

## 🚀 Пошаговая инструкция включения

### Шаг 1: Откройте Railway Dashboard
1. Перейдите на https://railway.app
2. Войдите в аккаунт
3. Откройте проект **ronix-inventory-system**
4. Выберите сервис **ronix-inventory-system** (не базу данных pacific-analysis!)

### Шаг 2: Перейдите в настройки переменных
1. В верхнем меню найдите вкладку **Variables**
2. Здесь вы увидите существующие переменные (DATABASE_URL и др.)

### Шаг 3: Добавьте email-переменные
Нажимайте **+ New Variable** и добавьте по одной:

**Переменная 1 - Email адрес:**
```
Variable Name: EMAIL_HOST_USER
Value: error04p@gmail.com
```
Нажмите **Add**

**Переменная 2 - Пароль приложения:**
```
Variable Name: EMAIL_HOST_PASSWORD
Value: yylwzszlqrmniixd
```
Нажмите **Add**

**Переменная 3 (опционально) - Отправитель:**
```
Variable Name: DEFAULT_FROM_EMAIL
Value: error04p@gmail.com
```
Нажмите **Add**

### Шаг 4: Дождитесь перезапуска
- Railway автоматически перезапустит сервис
- Процесс займет 2-3 минуты
- Статус изменится с "Building" → "Deploying" → "Active"

### Шаг 5: Проверьте работу
1. Перейдите на вкладку **Deploy Logs**
2. В логах должно появиться: `Using SMTP backend for email` (вместо console backend)
3. Создайте тестовую заявку на сайте
4. В логах увидите: `Email отправлен: Новая заявка #142 -> ['worker@email.com']`

---

## ✅ Какие уведомления будут работать

### 1. 📝 Новая заявка
- **Кому отправляется:** Всем работникам и администраторам
- **Когда:** При создании заявки клиентом
- **Что в письме:** Номер заявки, имя клиента, тип заявки, описание
- **Шаблон:** `templates/emails/new_order_notification.html`

### 2. 👤 Назначение исполнителя
- **Кому отправляется:** Назначенному работнику
- **Когда:** Когда администратор назначает ответственного на заявку
- **Что в письме:** Детали заявки, контакты клиента, срочность
- **Шаблон:** `templates/emails/order_assigned_notification.html`

### 3. 📦 Низкий остаток товара
- **Кому отправляется:** Всем работникам и администраторам
- **Когда:** Количество товара падает ниже минимального уровня
- **Что в письме:** Название товара, текущий остаток, минимальный порог
- **Шаблон:** `templates/emails/low_stock_notification.html`

### 4. ❌ Вход в систему (ОТКЛЮЧЕНО)
- **Статус:** Специально отключено
- **Причина:** Вызывало таймауты на Railway (120 секунд)
- **Файл:** `users/signals.py` - функция закомментирована (строки 9-30)

---

## 🔧 Технические детали

### Автоматический выбор backend
Система сама определяет, отправлять ли реальные письма:

```python
# ronix_project/settings.py строки 179-183
if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # ✅ Gmail
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # ❌ Логи
```

### Настройки SMTP для Gmail
- **Сервер:** smtp.gmail.com
- **Порт:** 587
- **Шифрование:** TLS
- **Таймаут:** 10 секунд
- **Fail silently:** True (ошибки не ломают сайт)

### Защита от ошибок
```python
# core/notifications.py строка 24
if not settings.EMAIL_HOST_USER:
    logger.info(f"Email не настроен, пропуск отправки: {subject}")
    return False
```

Если email не настроен, система работает нормально, просто без писем.

---

## 🧪 Как протестировать

### Тест 1: Создание заявки
1. Войдите как **client** (пароль: client123)
2. Создайте новую заявку на обслуживание
3. Проверьте логи Railway - должно быть "Email отправлен"
4. Проверьте почту error04p@gmail.com

### Тест 2: Назначение исполнителя
1. Войдите как **worker** (пароль: worker123)
2. Откройте любую новую заявку
3. Нажмите "Редактировать" и назначьте себя
4. Проверьте почту worker (если у него указан email в профиле)

### Тест 3: Низкий остаток
1. Войдите как **worker**
2. Перейдите в Склад → Комплектующие
3. Измените количество любого товара на 2 (меньше min_quantity = 5)
4. Работники получат уведомление

---

## ⚠️ Важные замечания

### Кому приходят письма?
Письма приходят **только пользователям с заполненным email**!

Проверьте:
1. Откройте Пользователи
2. Убедитесь, что у работника **worker** указан email
3. Если email пустой - добавьте его в профиле

### Почему письма в спаме?
- Gmail видит отправку как от приложения, а не настоящего пользователя
- Для продакшена используйте SendGrid, Mailgun или AWS SES
- Или настройте SPF/DKIM записи для домена

### Безопасность пароля
- `yylwzszlqrmniixd` - это **пароль приложения Gmail**, не основной пароль
- Его можно отозвать в любой момент в настройках Google
- Если вас взломают, меняйте только пароль приложения
- Никогда не коммитьте пароли в Git!

---

## 🔍 Просмотр статуса email в логах

### До настройки (console backend):
```
Using console backend for email
Email не настроен, пропуск отправки: Новая заявка #142
```

### После настройки (smtp backend):
```
Using SMTP backend for email
Email отправлен: Новая заявка #142 -> ['worker@example.com']
```

### При ошибке отправки:
```
Ошибка отправки email: [Errno 110] Connection timed out
```

---

## 🛠️ Альтернативные варианты

### Использовать Yandex Mail
```
EMAIL_HOST_USER = your-email@yandex.ru
EMAIL_HOST_PASSWORD = your-password
EMAIL_HOST = smtp.yandex.ru
```

### Использовать Mail.ru
```
EMAIL_HOST_USER = your-email@mail.ru
EMAIL_HOST_PASSWORD = your-password
EMAIL_HOST = smtp.mail.ru
```

### Использовать SendGrid (рекомендуется для продакшена)
1. Зарегистрируйтесь на sendgrid.com
2. Получите API ключ
3. Добавьте переменную:
```
EMAIL_BACKEND = anymail.backends.sendgrid.EmailBackend
ANYMAIL_SENDGRID_API_KEY = your-api-key
```

---

## 🐛 Устранение проблем

### Письма не приходят
**Проверка 1:** Логи Railway
```bash
# Должно быть:
Email отправлен: Новая заявка #142 -> ['email@example.com']

# А не:
Email не настроен, пропуск отправки
```

**Проверка 2:** Папка "Спам" в Gmail
- Gmail часто отправляет автоматические письма в спам
- Отметьте как "Не спам" один раз

**Проверка 3:** Email в профиле
- У пользователя **worker** должен быть указан email
- Зайдите в админку → Пользователи → worker → Email

### Ошибка "Authentication failed"
- Проверьте правильность `EMAIL_HOST_PASSWORD`
- Это должен быть пароль приложения (16 символов), не обычный пароль Gmail
- Сгенерируйте новый пароль: https://myaccount.google.com/apppasswords

### Таймауты (Connection timed out)
Увеличьте таймаут в Railway Variables:
```
EMAIL_TIMEOUT = 30
```

### Письма идут очень медленно
- Это нормально для Gmail (до 30 секунд)
- Для быстрой отправки используйте SendGrid или Mailgun

---

## 📚 Дополнительная информация

### Где находятся шаблоны писем?
```
templates/emails/
├── new_order_notification.html      # Новая заявка
├── order_assigned_notification.html # Назначение исполнителя
├── low_stock_notification.html      # Низкий остаток
└── login_notification.html          # Вход (не используется)
```

### Как изменить текст писем?
1. Откройте нужный шаблон в `templates/emails/`
2. Измените HTML по своему вкусу
3. Сохраните и запушьте на GitHub
4. Railway автоматически задеплоит изменения

### Как добавить новый тип уведомления?
1. Создайте функцию в `core/notifications.py`
2. Создайте HTML шаблон в `templates/emails/`
3. Вызовите функцию в нужном месте кода

### Где вызываются уведомления?
- **Новая заявка:** `orders/views.py` → `order_create` (строка 56)
- **Назначение:** `orders/views.py` → `order_edit` (строка 89)
- **Низкий остаток:** `inventory/views.py` → после изменения количества

---

## 📋 Чек-лист включения email

- [ ] Открыл Railway Dashboard
- [ ] Выбрал сервис ronix-inventory-system (не базу данных)
- [ ] Перешел на вкладку Variables
- [ ] Добавил EMAIL_HOST_USER = error04p@gmail.com
- [ ] Добавил EMAIL_HOST_PASSWORD = yylwzszlqrmniixd
- [ ] Дождался перезапуска сервиса (2-3 минуты)
- [ ] Проверил логи Deploy Logs - есть ли "Using SMTP backend"
- [ ] Создал тестовую заявку на сайте
- [ ] Проверил логи - есть ли "Email отправлен"
- [ ] Проверил почту error04p@gmail.com (включая спам)
- [ ] Убедился, что у worker указан email в профиле

---

**Создано:** 7 марта 2026  
**Версия:** Production с PostgreSQL на Railway  
**URL:** https://ronix-inventory-system-production.up.railway.app/  
**GitHub:** https://github.com/error04p124124/ronix-inventory-system
