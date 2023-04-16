# API_YaMDb
![Django-app workflow](https://github.com/stasemenov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр.
Читатели оставляют к произведениям отзывы и выставляют рейтинг (от 1 до 10).
Cредняя оценка произведения высчитывается автоматически.

**Аутентификация по JWT-токену**

Поддерживает методы GET, POST, PUT, PATCH, DELETE

## Стек технологий
- проект написан на Python с использованием Django REST Framework
- библиотека Simple JWT - работа с JWT-токеном
- библиотека django-filter - фильтрация запросов
- база данных - PostgreSQL
- система управления версиями - git

## Как запустить проект:

- Склонируйте репозиторий:

```
git clone git@github.com:sapphirehead/infra_sp2.git
```

- Создайте файл .env
```
nano infra_sp2/infra/.env
```

- И установите переменные окружения:
```
TOKEN=  # Django SECRET_KEY
DB_ENGINE=django.db.backends.postgresql
DB_NAME=  # Имя БД
POSTGRES_USER=  # Пользователь
POSTGRES_PASSWORD=  # Пароль
DB_HOST=  # Хост
DB_PORT=  # Порт
```

- Разверните контейнеры:

```
cd infra
docker-compose up -d --build
```

- Выполните эти команды:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

- Загрузите данные из дампа:
```
docker-compose exec web python manage.py loaddata fixtures.json
```

__________________________________

Ваш проект запустился на http://yamdb.stanislavsemenov.ru/

Полная документация доступна по адресу http://158.160.40.250/redoc/


### Cоздан в команде из трёх человек с использованим Git в рамках учебного курса Яндекс.Практикум.

- Иван Молотков https://github.com/UserVeryFriendly
- Людмила Глушкова https://github.com/Ludmila-Glushkova
- Станислав Семёнов https://github.com/stasemenov