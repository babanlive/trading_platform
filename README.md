## Описание проекта

Проект представляет из себя веб-приложение, с помощью которого люди смогут для управлять продуктами на торговой площадке.

## Функциональность:

- Добавление, обновление, удаление и получение информации о продуктах.
- Получение списка продуктов с фильтрацией по категориям и цене.
- CRUD операции для категорий продуктов.

## Технологии и инструменты

- Python 3.12
- FastAPI
- Pre-commit
- Ruff
- Postgres
- Docker


## Установка и запуск проекта

1. Клонируйте репозиторий и перейдите в папку проекта:
```shell
git clone git@github.com:babanlive/trading_platform.git && cd trading_platform
```

2. Создание файла .env
- Создайте в папке приложения файл `.env` согласно образцу [.env_example](.env.example)

3. Запуск проекта через Docker
- Для запуска в режиме разработки выполните команду:
```shell
docker-compose -f docker compose.dev.yaml up --build
```

4. Выполните миграции
```shell
docker exec -it app_fastapi poetry run alembic upgrade head
```

 ## Работа с API:
- Базовый URL

API доступно по адресу:
```shell
http://127.0.0.1:8000/api/v1/
```
- GET /products — Получение списка продуктов с поддержкой фильтрации.

- POST /products — Добавление нового продукта.

- PUT /products/{product_id} — Обновление информации о продукте.

- DELETE /products/{product_id} — Удаление продукта.


- GET categories — Получение списка категорий.

- POST /categories — Добавление новой категории.

- PUT /categories/{category_id} — Обновление информации о продукте.

- DELETE categories/{category_id} — Удаление категории.

## Пример запроса

- Создание категории

```shell
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/categories' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Fruits"
}'
```

- Добавление продукта

```shell
curl -X 'POST' \                                    
  'http://127.0.0.1:8000/api/v1/products' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Banana",
  "description": "price for 1kg bananas",
  "price": 175,
  "image_url": "http://example_picture.com/banana.png",
  "category_id": 1
}'
```
- Получение продуктов с фильтрацией.

```shell
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/products?category_id=3&min_price=100' \
  -H 'accept: application/json'
  ```
  
  ## Тесты
1. Создайте тестовую БД

    ```shell
    docker exec -it pg_db psql -U user -d postgres -c "CREATE DATABASE test_db;"
    ```

2. Запустите тесты:

    ```shell
    docker exec -it app_fastapi poetry run pytest -v tests/ --disable-warnings
    ```
