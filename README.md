# Сайт объявлений

Добро пожаловать в проект **Сайт объявлений**, созданный на основе Django! Это приложение предоставляет удобный инструмент для размещения и управления объявлениями с широким спектром возможностей для пользователей и администраторов.

## Основные возможности

- **Удобный поиск**: Ищите объявления с помощью ключевых фильтров, таких как категории, цена, местоположение и дата публикации.
- **Панель администратора**: Управление пользователями, объявлениями и модерация контента через удобный интерфейс.
- **Авторизация и регистрация**: Возможность создания учетной записи через электронную почту и пароль.
- **Профили пользователей**:
  - Указание контактной информации.
  - Возможность загрузить аватар.
- **Публикация объявлений**:
  - Пользователи могут создавать свои объявления.
  - Администратор проверяет и утверждает объявления перед их публикацией.

## Стек технологий

Проект разработан с использованием следующих технологий:
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **База данных**: SQLite 
- **Аутентификация**: Django Auth

## Установка и запуск

1. Клонируйте репозиторий:
  ```bash
  git clone https://github.com/IgloBruh/ads_project.git
  ```
2. Перейдите в папку проекта:
  ```bash
  cd ads_project
  ```
3. Создайте и активируйте виртуальное окружение:
  ```bash
  python -m venv venv
  source venv/bin/activate   # для Linux/Mac
  venv\Scripts\activate      # для Windows
  ```
4. Установите зависимости:
  ```bash
  pip install -r requirements.txt
  ```
5. Выполните миграции базы данных:
  ```bash
  python manage.py migrate
  ```
6. Запустите сервер разработки:
  ```bash
  python manage.py runserver
  ```
   
Теперь сайт доступен по адресу http://127.0.0.1:8000/.

## Как внести вклад?

Если у вас есть идеи для улучшения проекта, не стесняйтесь создавать pull request'ы или открывать issues в репозитории.
