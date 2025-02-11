# Avito Merch

> [Техническое задание](./TASKS.md)

---

## Описание проекта

Этот сервис позволяет сотрудникам приобретать мерч за внутреннюю валюту (монеты), а также передавать монеты друг другу.
Каждый новый сотрудник получает 1000 монет.

Функционал API:

- Авторизация и получение JWT-токена
- Просмотр баланса монет, инвентаря и истории транзакций
- Покупка товаров из внутреннего магазина
- Перевод монет между пользователями

---

## Стек технологий

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Alembic
- Docker
- Pytest
- Locust

---

## Как запустить контейнер

1. Клонировать репозиторий:

```
git clone https://github.com/yuldashov10/avito_merch_store.git && cd avito_merch_store
```

2. Собрать и запустить контейнеры:

```
docker compose up --build
```

- После успешного запуска сервис будет доступен на http://localhost:8080

3. Применить миграции

```
docker compose exec web alembic revision --autogenerate -m "Initial commit"
```

```
docker compose exec web alembic upgrade head
```

```
docker compose exec web python init_merch.py
```

---

## Документация API

После запуска сервиса можно открыть документацию OpenAPI:

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

---

## Как запустить тесты

Запуск юнит-тестов:

```
docker compose exec web pytest tests/
```

Запуск тестов с покрытием кода:

```
docker compose exec web pytest --cov=avito_merch tests/
```

---

## Как запустить нагрузочное тестирование

1. Запуск Locust в контейнере:

```
docker compose exec web locust -f locustfile.py
```

> Интерфейс Locust в браузере - http://localhost:8089

```
Host: http://localhost:8080
Number of users: 1000
Spawn rate: 1
```

---

## Автор:

Шохрух Юлдашов | [Telegram](t.me/shyuldashov)
