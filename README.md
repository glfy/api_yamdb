# Описание:

Проект YaMDb собирает отзывы пользователей на различные произведения.

## Команда разработки:

1) [glfy - Тимлид](https://github.com/glfy)
2) [Grandkol](https://github.com/Grandkol)
3) [Artgele](https://github.com/artgele)

## Как запустить проект

1. Клонировать репозиторий и перейти в него в командной строке:

   ```bash
   git clone git@github.com:glfy/api_yamdb.git
   cd api_yamdb

2. Cоздать и активировать виртуальное окружение:

   ```bash
   python3 -m venv env
   source env/bin/activate

3. Установить зависимости из файла requirements.txt:

   ```bash
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt

4. Выполнить миграции:

   ```bash
   python3 manage.py migrate
   
5. Добавить тестовые данные в бд:

   ```bash
   python3 manage.py import_csv

5. Запустить проект:

   ```bash
   python3 manage.py runserver

## Примеры запросов.

```
POST http://127.0.0.1:8000/api/v1/auth/signup/ - Получить код подтверждения на переданный email.

{
  "email": "user@example.com",
  "username": "string"
}
```

```
POST http://127.0.0.1:8000/api/v1/auth/token/ - Получение JWT-токена в обмен на username 
и confirmation code. 

{
  "username": "string",
  "confirmation_code": "string"
}
```

```
GET http://127.0.0.1:8000/api/v1/categories/ - Категории (типы) произведений

{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

```
POST http://127.0.0.1:8000/api/v1/categories/ - Создать категорию. 

{
  "name": "string",
  "slug": "string"
}
```

```
GET http://127.0.0.1:8000/api/v1/genres/ - Получить список всех жанров.

{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```