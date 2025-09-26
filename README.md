# Инструкция по запуску
1. Установка зависимостей

Создание виртуального окружения

python -m venv venv

venv\Scripts\activate  # Windows

source venv/bin/activate  # Linux/Mac

pip install django

2. Настройка базы данных

Применение миграций

python manage.py makemigrations

python manage.py migrate

4. Запуск веб-сервиса
python manage.py runserver

Приложение будет доступно по адресу: http://127.0.0.1:8000/
