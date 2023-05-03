# Как запустить проект

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
