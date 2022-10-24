
# Проект Foodgram
![foodgram_workflow](https://github.com/korecbtc/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Описание
Foodgram, «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Поддерживает методы GET, POST, PUT, PATCH, DELETE

Предоставляет данные в формате JSON

Cоздан в качестве дипломного проекта в рамках учебного курса Яндекс.Практикум.
### Запуск проекта:

- Клонируйте репозиторий:
```
git clone git@github.com:korecbtc/foodgram-project-react.git
```
 - Перейдите в папку с проектом

 - Установите и активируйте виртуальное окружение:
```
python -m venv venv

source venv/Scripts/activate
```

 - Зайдите в папку backend и установите зависимости из файла requirements.txt

``` 
pip install -r requirements.txt
```

- В папке с файлом manage.py выполните команды:

``` 
python manage.py makemigrations 

python manage.py migrate

python manage.py runserver 
```
- В папке frontend в файле package.json пропишите "proxy": "http://127.0.0.1:8000/"
<<<<<<< HEAD
```
- Запустите фронтенд

```
***

# Технологии
- бэкенд написан на Python с использованием Django REST Framework
- фронтенд написан на фреймворке React
# Автор
=======

- Запустите фронтенд

***

# Технологии

- бэкенд написан на Python с использованием Django REST Framework
- фронтенд написан на фреймворке React

# Автор

>>>>>>> 1d2cbe24c27c8da58a492e56ba0e7935a26313db
Корец Иван
