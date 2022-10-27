
# Проект Foodgram
![foodgram_workflow](https://github.com/korecbtc/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Стек технологий
- Django
- Django Rest Framework
- Docker
- Docker-compose
- Gunicorn
- Nginx
- PostgreSQL

## Описание
Foodgram, «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Поддерживает методы GET, POST, PUT, PATCH, DELETE
Предоставляет данные в формате JSON

Cоздан в качестве дипломного проекта в рамках учебного курса Яндекс.Практикум.
### Подготовка и запуск проекта
- Установите Docker и зарегистрируйтесь на [DockerHub](https://hub.docker.com/)
- Клонируйте проект. 
```bash
git clone git@github.com:korecbtc/foodgram-project-react.git
```
- Из папки /foodgram-project-react/frontend выполните команду:
```bash
sudo docker build -t <логин на DockerHub>/<название образа)> .
```
- Выложите этот образ на DockerHub
- Измените названия контейнеров в файлах docker-compose.yml и nginx.conf которые находятся в директории infra/ и foodgram_workflow.yml в папке .github/workflows/.
При необходимости добавьте/измените адреса проекта в файле nginx.conf
- Выполните вход на удаленный сервер
- Установите docker на сервер:
```bash
sudo apt install docker.io 
```
- Установите docker-compose на сервер:
```bash
sudo apt-get update
sudo apt install docker-compose
```
- Скопируйте файл docker-compose.yml и nginx.conf из директории infra на сервер:
```bash
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
```
- Для работы с Workflow пропишите в Secrets GitHub переменные окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID своего телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```
- Сделайте коммит и пулл в git, дождитесь выполнения всех Actions.
- Зайдите на боевой сервер и выполните команды:
    ```bash
    sudo docker-compose exec backend python manage.py migrate
    ```
    ```bash
    sudo docker-compose exec backend python manage.py collectstatic --no-input 
    ```
    ```bash
    sudo docker-compose exec backend python manage.py createsuperuser
    ```

    ```bash
    sudo docker-compose exec backend bash

    python manage.py import_csv
    ```

- Проект будет доступен по вашему IP-адресу.

### Документация
Подробная документация API будет доступна по адресу - http://<IP-адрес вашего сервера>/api/docs/

### Автор бэкенд-части


Корец Иван
https://github.com/korecbtc
