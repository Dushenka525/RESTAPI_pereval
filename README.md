# REST API для проекта ФСТР (Перевалы)

## Описание
Данный REST API предназначен для взаимодействия мобильного приложения с базой данных перевалов. API позволяет:
- загружать изображения;
- создавать, просматривать и редактировать записи о перевалах;
- отслеживать статус модерации записи.

Проект разработан на Django + Django REST Framework, использует PostgreSQL.

## Технологии
- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL
- python-dotenv (для переменных окружения)

## Установка и настройка

1. **Клонировать репозиторий**
   ```bash
   git clone https://github.com/Dushenka525/RESTAPI_pereval.git
   cd your-repo

2. **Создать и клонировать git репозиторий**
python -m venv venv
source venv/bin/activate      # для Linux/Mac
venv\Scripts\activate          # для Windows

3. **Установить зависимости**
pip install -r requirements.txt

4. **Настроить переменные окружения**
Создать файл .env в корне проекта (рядом с manage.py) со следующим содержимым:

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_django_secret_key
DEBUG=True

5. **Выполнить миграции**
python manage.py migrate

6. **Запустить сервер разработки**
python manage.py runserver

**Модели данных (кратко)**
Tourist — данные туриста (email, телефон, ФИО).
Coords — координаты перевала (широта, долгота, высота).
Image — загруженное изображение (файл, название, дата загрузки).
PerevalAdded — запись о перевале (названия, дата, координаты, пользователь, уровни сложности, статус модерации).
PerevalImage — связь перевала и изображения (многие-ко-многим).

Статусы модерации:

new — новый (по умолчанию)
pending — на модерации
accepted — принят
rejected — отклонён

**API Endpoints**

1. **Загрузка изображения**

Пример запроса Postman
Установите метод POST.
Введите URL:http://127.0.0.1:8000/api/images/
Перейдите на вкладку Body.

Выберите опцию form-data.
В колонке KEY введите image.
В колонке TYPE выберите File (справа от поля KEY).
В колонке VALUE нажмите "Select Files" и выберите нужный файл на вашем компьютере.
Нажмите Send.

Успешный ответ (201 Created):
{
    "id": 1,
    "title": "Вершина",
    "url": "/media/images/photo_20250305.jpg"
}

2. **Создание нового перевала**
URL: /api/submitData/
Метод: POST
Тело запроса (json)
{
    "beautyTitle": "пер. ",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "add_time": "2025-03-04T15:30:00+03:00",
    "user": {
        "email": "ivan@example.com",
        "phone": "+7-912-345-67-89",
        "fam": "Петров",
        "name": "Иван",
        "otc": "Сергеевич"
    },
    "coords": {
        "latitude": 49.9876,
        "longitude": 86.5432,
        "height": 3150
    },
    "winter_level": "2А",
    "summer_level": "1Б",
    "autumn_level": "1А",
    "spring_level": "",
    "images": [1]
}

Удачный ответ
{
    "status": 200,
    "message": "Отправлено успешно",
    "id": 42
}


Ошибка валидации (400 Bad Request):

{
    "status": 400,
    "message": "Ошибка валидации",
    "errors": {
        "title": ["This field is required."]
    }
}

3. **Получение списка перевалов пользователя по email**

URL: /api/submitData/?user__email=<email>
Метод: GET

Успешный ответ (200 OK):

[
    {
        "id": 42,
        "beautyTitle": "пер. ",
        "title": "Пхия",
        "other_titles": "Триев",
        "connect": "",
        "add_time": "2025-03-04T15:30:00+03:00",
        "user": {
            "email": "ivan@example.com",
            "phone": "+7-912-345-67-89",
            "fam": "Петров",
            "name": "Иван",
            "otc": "Сергеевич"
        },
        "coords": {
            "latitude": 49.9876,
            "longitude": 86.5432,
            "height": 3150
        },
        "winter_level": "2А",
        "summer_level": "1Б",
        "autumn_level": "1А",
        "spring_level": "",
        "status": "new",
        "images": [
            {
                "id": 1,
                "title": "Вершина",
                "image": "/media/images/photo1.jpg",
                "date_added": "2025-03-05T10:00:00Z"
            }
        ]
    }
]


Если пользователь не найден, возвращается пустой массив [].

Ошибка (400 Bad Request) — если параметр user__email не указан:


{
    "state": 0,
    "message": "Не указан параметр user__email"
}


4. **Получение детальной информации о перевале по ID**

URL: /api/submitData/<id>/
Метод: GET


Пример запроса:
GET /api/submitData/42/

Ответ аналогичен структуре объекта в списке выше.

Ошибка (404 Not Found):

{
    "state": 0,
    "message": "Объект не найден"
}

5. **Редактирование перевала (только если статус new)**

URL: /api/submitData/<id>/
Метод: PATCH

Тело запроса
{
    "title": "Новое название",
    "coords": {
        "latitude": 50.0,
        "height": 3200
    }
}

Успешный ответ (200 OK):

json
{
    "state": 1,
    "message": "Запись успешно обновлена"
}


Ошибки:

Если статус не new:

{
    "state": 0,
    "message": "Редактирование запрещено, статус не 'new'"
}


Ошибки:

Если статус не new:

{
    "state": 0,
    "message": "Редактирование запрещено, статус не 'new'"
}

Ошибка валидации (400):

json
{
    "state": 0,
    "message": "Ошибка валидации",
    "errors": {
        "coords": {
            "latitude": ["A valid number is required."]
        }
    }
}



**Коды ответов**
200 OK — запрос выполнен успешно.
201 Created — ресурс создан (для изображений).
400 Bad Request — ошибка валидации или неверные параметры.
404 Not Found — ресурс не найден.
405 Method Not Allowed — метод не поддерживается для данного URL.
500 Internal Server Error — ошибка на стороне сервера.


**Примечания**
При создании перевала поле status автоматически устанавливается в new.