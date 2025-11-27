# 🚀 Быстрый старт

Краткая инструкция для быстрого запуска Coffee Shop API.

## Шаг 1: Установка зависимостей

```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

## Шаг 2: Настройка базы данных

```bash
# Создать базу данных в PostgreSQL
createdb coffee_shop

# Или через psql:
psql -U postgres
CREATE DATABASE coffee_shop;
\q
```

## Шаг 3: Настройка переменных окружения

```bash
# Скопировать example файл
cp env.example .env

# Отредактировать .env (указать свои данные БД)
# DATABASE_URL=postgresql://user:password@localhost:5432/coffee_shop
```

## Шаг 4: Инициализация данных

```bash
# Создать админа
python scripts/init_admin.py

# Заполнить демо-данными (опционально)
python scripts/seed_data.py
```

## Шаг 5: Запуск сервера

```bash
python main.py
```

## Шаг 6: Тестирование

Откройте в браузере:
- API документация: http://localhost:8000/docs
- Альтернативная документация: http://localhost:8000/redoc

## 🔐 Тестовые учетные записи

После выполнения скриптов:

**Администратор:**
- Email: `admin@coffeeshop.com`
- Password: `admin123`

**Пользователь:**
- Email: `demo@coffeeshop.com`
- Password: `demo123`

## 📋 Быстрый тест API

### 1. Получить токен (Login)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@coffeeshop.com&password=admin123"
```

### 2. Получить список товаров

```bash
curl "http://localhost:8000/api/v1/products/"
```

### 3. Создать заказ

```bash
curl -X POST "http://localhost:8000/api/v1/orders/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "delivery_address": "Moscow, Red Square",
    "phone": "+79991234567",
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 2, "quantity": 1}
    ]
  }'
```

## 🐳 Docker (Альтернативный способ)

```bash
# Запустить все сервисы
docker-compose up -d

# Проверить логи
docker-compose logs -f api

# Остановить
docker-compose down
```

## ⚠️ Troubleshooting

### База данных не подключается
- Проверьте, что PostgreSQL запущен
- Проверьте правильность DATABASE_URL в .env

### Ошибка импорта модулей
- Убедитесь, что виртуальное окружение активировано
- Переустановите зависимости: `pip install -r requirements.txt`

### Порт 8000 уже занят
- Измените порт в main.py или при запуске:
  ```bash
  uvicorn main:app --port 8080
  ```

## 📚 Дополнительная информация

Полная документация: [README.md](README.md)

