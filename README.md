# shop_project
### Описание:
Shop API - проект интернет-магазина продуктов в котором реализованы:
- Просмотр категорий и подкатегорий продуктов
- Просмотр списка продуктов
- Возможность добавления продукта в корзину
- Возможность изменения количества/удаления/полной очистки корзины продуктов
- Простотр состава и итоговой стоимости корзины продуктов

### Технологии:

[![name badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![name badge](https://img.shields.io/badge/Django-3776AB?logo=django&logoColor=white)](https://docs.djangoproject.com/en/4.2/releases/3.2/)
[![name badge](https://img.shields.io/badge/Django_REST_framework-3776AB?logo=djangorestramework&logoColor=white)](https://www.django-rest-framework.org/)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Anna9449/shop_project.git
```

```
cd shop_project
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Создать файл .env и заполните его своими данными, пример: 

```
SECRET_KEY=*** # Секретный ключ Django (без кавычек)
DEBUG=True # Выбрать режим отладки
ALLOWED_HOSTS=*** # Список разрешённых хостов (через запятую и без пробелов)
SQLITE_DB = db.sqlite3
```

Запустить проект:

```
python3 manage.py runserver
```

### Документация к API:

### Автор
[![name badge](https://img.shields.io/badge/Anna_Pestova-3776AB?logo=github&logoColor=white)](https://github.com/Anna9449)
