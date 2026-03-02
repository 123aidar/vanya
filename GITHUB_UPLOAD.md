# 📤 Инструкция по загрузке проекта на GitHub

## Вариант 1: Через командную строку (рекомендуется)

### Шаг 1: Инициализация Git репозитория

Откройте PowerShell в папке проекта `d:\ronix` и выполните:

```powershell
# Перейдите в папку проекта
cd d:\ronix

# Инициализируйте Git репозиторий
git init

# Добавьте все файлы
git add .

# Создайте первый коммит
git commit -m "Initial commit: Система управления запасами ООО НПФ Роникс-Л"
```

### Шаг 2: Создание репозитория на GitHub

1. Откройте https://github.com/
2. Войдите в аккаунт
3. Нажмите **"+"** в правом верхнем углу → **"New repository"**
4. Заполните форму:
   - **Repository name:** `ronix-inventory-system` (или любое другое имя)
   - **Description:** "Информационная система управления запасами и комплектующими в ООО НПФ Роникс-Л"
   - **Visibility:** Private или Public (на ваш выбор)
   - ⚠️ **НЕ СОЗДАВАЙТЕ** README.md, .gitignore или LICENSE (они уже есть в проекте)
5. Нажмите **"Create repository"**

### Шаг 3: Связывание локального репозитория с GitHub

После создания репозитория GitHub покажет команды. Выполните в PowerShell:

```powershell
# Добавьте удаленный репозиторий (замените YOUR-USERNAME и REPO-NAME)
git remote add origin https://github.com/YOUR-USERNAME/REPO-NAME.git

# Отправьте код на GitHub
git branch -M main
git push -u origin main
```

**Пример:**
```powershell
git remote add origin https://github.com/johndoe/ronix-inventory-system.git
git branch -M main
git push -u origin main
```

### Шаг 4: Ввод учетных данных

GitHub попросит ввести:
- **Username:** ваш логин на GitHub
- **Password:** используйте **Personal Access Token** (не обычный пароль!)

#### Как получить Personal Access Token:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Выберите срок действия и права доступа: `repo` (полный доступ к репозиториям)
4. Скопируйте сгенерированный токен
5. Используйте его вместо пароля при `git push`

---

## Вариант 2: Через GitHub Desktop (для новичков)

### Шаг 1: Установка GitHub Desktop

1. Скачайте с https://desktop.github.com/
2. Установите и войдите в аккаунт GitHub

### Шаг 2: Добавление проекта

1. Откройте GitHub Desktop
2. File → Add Local Repository
3. Выберите папку `d:\ronix`
4. Если Git не инициализирован, нажмите "Create a repository"

### Шаг 3: Создание коммита

1. В левом столбце отметьте все файлы
2. Внизу введите сообщение коммита: "Initial commit"
3. Нажмите "Commit to main"

### Шаг 4: Публикация на GitHub

1. Нажмите "Publish repository" вверху
2. Выберите имя и description
3. Выберите Public или Private
4. Нажмите "Publish repository"

---

## ⚠️ ВАЖНО: Безопасность

### Проверьте, что .env не попадет в Git:

Файл `.gitignore` уже настроен правильно, но убедитесь:

```powershell
# Проверьте содержимое .gitignore
cat .gitignore
```

Должна быть строка: `.env`

### Что НЕ должно попасть в Git:

- ✅ `.env` (секретные ключи)
- ✅ `db.sqlite3` (база данных)
- ✅ `venv/` (виртуальное окружение)
- ✅ `media/` (загруженные файлы)
- ✅ `staticfiles/` (собранная статика)
- ✅ `*.pyc`, `__pycache__/` (скомпилированные файлы)

### Что ДОЛЖНО попасть в Git:

- ✅ `.env.example` (пример настроек)
- ✅ `.gitignore`
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ Весь код приложений
- ✅ `templates/` и `static/` (исходники)

---

## 📝 После загрузки на GitHub

### Проверьте репозиторий:

1. Откройте репозиторий на GitHub
2. Убедитесь, что видны все файлы
3. Проверьте, что `.env` **НЕ** загружен
4. README.md должен отображаться на главной странице

### Полезные команды Git:

```powershell
# Проверка статуса файлов
git status

# Добавление изменений
git add .

# Создание коммита
git commit -m "Описание изменений"

# Отправка на GitHub
git push

# Обновление с GitHub
git pull

# Просмотр истории
git log --oneline

# Создание новой ветки
git checkout -b feature-name

# Переключение между ветками
git checkout main
```

---

## 🚀 Деплой на Railway (опционально)

После загрузки на GitHub можете задеплоить на Railway:

### Шаг 1: Подключение GitHub к Railway

1. Откройте https://railway.app/
2. Войдите через GitHub
3. New Project → Deploy from GitHub repo
4. Выберите ваш репозиторий

### Шаг 2: Настройка переменных окружения

В Railway добавьте переменные:

```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.railway.app
RAILWAY_PUBLIC_DOMAIN=your-domain.railway.app

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Шаг 3: Deploy

Railway автоматически:
- Установит зависимости из `requirements.txt`
- Запустит `python manage.py collectstatic --noinput`
- Запустит `gunicorn` согласно `Procfile`

---

## 🔧 Обновление проекта на GitHub

После внесения изменений в код:

```powershell
# 1. Проверьте, что изменилось
git status

# 2. Добавьте изменения
git add .

# 3. Создайте коммит с описанием
git commit -m "Добавлены email-уведомления"

# 4. Отправьте на GitHub
git push
```

---

## 📚 Дополнительные ресурсы

- **Git документация:** https://git-scm.com/doc
- **GitHub Guides:** https://guides.github.com/
- **Railway Docs:** https://docs.railway.app/
- **Django Deployment:** https://docs.djangoproject.com/en/5.0/howto/deployment/

---

## ❓ Часто задаваемые вопросы

### Q: Как удалить файл из Git, если он попал по ошибке?

```powershell
# Удалить из Git, но оставить локально
git rm --cached filename

# Добавить в .gitignore
echo "filename" >> .gitignore

# Закоммитить изменения
git add .gitignore
git commit -m "Remove sensitive file"
git push
```

### Q: Что делать, если случайно залил .env?

```powershell
# 1. Удалите файл из Git
git rm --cached .env

# 2. Проверьте .gitignore
cat .gitignore  # должна быть строка .env

# 3. Закоммитьте
git commit -m "Remove .env from Git"
git push

# 4. ВАЖНО: Смените все секретные ключи в .env!
```

### Q: Как создать новую ветку для работы?

```powershell
# Создать и переключиться на новую ветку
git checkout -b feature/email-notifications

# Работайте в ветке
# ... делаете изменения ...

# Коммитьте и пушьте ветку
git add .
git commit -m "Add email notifications"
git push -u origin feature/email-notifications

# На GitHub создайте Pull Request
```

---

## ✅ Чеклист перед загрузкой

- [ ] `.gitignore` настроен правильно
- [ ] `.env` в .gitignore
- [ ] `.env.example` создан и документирован
- [ ] `requirements.txt` актуален
- [ ] `README.md` содержит описание проекта
- [ ] Удалены все `db.sqlite3`, `*.pyc`, `__pycache__/`
- [ ] Нет паролей и секретных ключей в коде
- [ ] Все коммиты имеют понятные описания

---

**Готово!** Теперь ваш проект на GitHub 🎉
