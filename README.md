# Notifications - Сервис уведомлений.

[//]: # (![workflow]&#40;https://github.com/artemis1359/foodgram-project-react/actions/workflows/main.yml/badge.svg&#41;)


## Описание проекта
Notifications — сервис управления рассылками API администрирования и получения статистики.

## Технологии

- [Python 3.9](https://www.python.org/downloads/)
- [Django 4.2.9](https://www.djangoproject.com/)
- [Django Rest Framewok 3.14](https://www.django-rest-framework.org/)
- [PostgreSQL](https://postgrespro.ru/docs/postgresql)
- [Nginx](https://nginx.org/ru/)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Redis](https://redis.io/)
 
## Установка проекта на локальный компьютер из репозитория 
 - Клонировать репозиторий `git clone git@github.com:Artemis1359/Notifications.git`
 - перейти в директорию с клонированным репозиторием
 - в корневой директории создайте файл .env
 - в файле .env прописать ваши данные
 - установить виртуальное окружение `python3 -m venv venv`
 - активировать виртуальное окружение `source venv/bin/activate` (Linux/masOS), `source venv/Scripts/activate` (Windows)
 - установить зависимости `pip install -r requirements.txt`
 - выполнить миграции `python3 manage.py migrate`
 - запустить сервер `python3 manage.py runserver`
 - запустить Celery `celery --app=Notifications worker -l INFO`
 - запустить flower `celery --app=Notifications flower --port=5555 broker=redis://redis:6379/0`

### Запуск через Docker Compose
 - Клонировать репозиторий `git clone git@github.com:Artemis1359/Notifications.git`
 - перейти в директорию с клонированным репозиторием
 - в корневой директории создайте файл .env
 - в файле .env прописать ваши данные
 - запустить контейнеры `sudo docker-compose up -d`
 - остановка контейнеров `sudo docker-compose stop`

```http://127.0.0.1:8000/api/v1/``` - api проекта

```http://127.0.0.1:8000/api/v1/clients/``` - клиенты

```http://127.0.0.1:8000/api/v1/mailings/``` - рассылки

```http://127.0.0.1:8000/api/v1/mailings/fullinfo/``` - общая статистика по всем рассылкам

```http://127.0.0.1:8000/api/v1/mailings/<pk>/info/``` - детальная статистика по конкретной рассылке

```http://127.0.0.1:8000/api/v1/messages/``` - сообщения

```http://127.0.0.1:8000/api/docs/``` - документация проекта

```http://127.0.0.15555``` - celery flower

### Дополнительные задания:
- Организовать тестирование написанного кода
- Подготовить docker-compose для запуска всех сервисов проекта одной командой
- Сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API. Пример: https://petstore.swagger.io
- Реализовать администраторский Web UI для управления рассылками и получения статистики по отправленным сообщениям
- Удаленный сервис может быть недоступен, долго отвечать на запросы или выдавать некорректные ответы. Необходимо организовать обработку ошибок и откладывание запросов при неуспехе для последующей повторной отправки. Задержки в работе внешнего сервиса никак не должны оказывать влияние на работу сервиса рассылок.

## Автор
Потапов Артем - [GitHub](https://github.com/artemis1359)