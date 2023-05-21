![Foodgram project](https://github.com/log1s7/foodgram-project-react/actions/workflows/foodgram-workflow.yml/badge.svg)

# **Foodgram project**

### _Продуктовый помощник_

# Описание

**«Продуктовый помощник»** - это сайт, на котором пользователи могут _публиковать_ рецепты, добавлять чужие рецепты в _избранное_ и _подписываться_ на публикации других авторов. Сервис **«Список покупок»** позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

# Проект

Проект развернут по адресу:
- http://51.250.87.223/

# Данные суперпользователя для теста админ панели

- email: admin@admin.ru
- password: admin

# Документация

Для просмотра документации к API перейдите по адресу:
- http://51.250.87.223/api/docs/

# Локальная установка

Установите на сервере docker и docker-compose.

Клонируйте репозиторий и перейдите в него в командной строке:
```sh
git clone https://github.com/log1s7/foodgram-project-react.git && cd foodgram-project-react
```
Перейдите в директорию с файлом _Dockerfile_ и запустите сборку образа:
```sh
cd backend && docker build -t <DOCKER_USERNAME>/foodgram:<tag> .
```
Перейдите в директорию с файлом _docker-compose.yml_:
```sh
cd ../infra
```
Создайте .env файл:
```sh
#.env
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
SECRET_KEY=<секретный ключ проекта django>
```
Запустите контейнеры:
```sh
docker-compose up -d --build
```
После успешного запуска контейнеров выполните миграции в проекте:
```sh
docker-compose exec backend python manage.py migrate
```
Создайте суперпользователя:
```sh
docker-compose exec backend python manage.py createsuperuser
```
Соберите статику:
```sh
docker-compose exec backend python manage.py collectstatic --no-input
```
Наполните БД заготовленными данными через интерфейс админ панели:

- Зайдите в Тэги/Ингредиенты в админ панели
- Нажмите импортировать в правом верхнем углу
- Выберите файл tags.json/ingredients.json в репозитории из папки foodgram-project-react/data

Создайте дамп (резервную копию) базы данных:
```sh
docker-compose exec backend python manage.py dumpdata > fixtures.json
```
Для остановки контейнеров и удаления всех зависимостей воспользуйтесь командой:
```sh
docker-compose down -v
```
