# Проектная работа: диплом

[Ссылка на репозиторий](https://github.com/sevrn73/graduate_work)

Участники @sevrn73, @rachet2012

## Запуск проекта

- Запустим docker-compose

```
docker-compose up
```

- Все миграции пройдут автоматически

## Доступные сервисы

- [Админ панель django](http://localhost/admin/)
- [Cinema together API](http://localhost/api/openapi)
- [AuthOpenAPI](http://localhost/auth_api/docs/)

## Запуск тестов AuthApi

```
docker-compose exec auth_api pytest
```
