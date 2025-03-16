![Version](https://img.shields.io/badge/version-v0.1.0--PreAlpha-orange)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.8.10-blue)
![Django](https://img.shields.io/badge/Django-4.2.19-green)

# Cafe Order Management System

📌 Система управления заказами в кафе.

## 📚 Оглавление
- [Cafe Order Management System](#cafe-order-management-system)
  - [📚 Оглавление](#-оглавление)
  - [📌 О проекте](#-о-проекте)
  - [🚀 Версия](#-версия)
  - [🛠 Технологии](#-технологии)
  - [🔧 Установка и запуск](#-установка-и-запуск)
    - [Клонирование репозитория](#клонирование-репозитория)
    - [Установка виртуального окружения](#установка-виртуального-окружения)
      - [Установка Python](#установка-python)
      - [Создание и активация виртуального окружения](#создание-и-активация-виртуального-окружения)
    - [Запуск в локальной среде](#запуск-в-локальной-среде)
      - [1. Установка зависимостей](#1-установка-зависимостей)
      - [2. Миграция базы данных](#2-миграция-базы-данных)
      - [3. (Опционально) Загрузка тестовых данных меню](#3-опционально-загрузка-тестовых-данных-меню)
      - [4. Запуск сервера](#4-запуск-сервера)
    - [Развертывание с Docker](#развертывание-с-docker)
  - [✅ Текущий функционал](#-текущий-функционал)
  - [✅ Базовая аутентификация](#-базовая-аутентификация)
  - [🔧 Запланированные функции](#-запланированные-функции)
  - [📌 API Endpoints](#-api-endpoints)
    - [📌 Основные](#-основные)
    - [📦 Orders API (Работа с заказами и блюдами)](#-orders-api-работа-с-заказами-и-блюдами)
      - [📌 Meal Endpoints](#-meal-endpoints)
      - [📌 Order Endpoints](#-order-endpoints)
    - [🛒 Basket API (Корзина)](#-basket-api-корзина)
    - [💳 Order Actions API (Действия с заказами)](#-order-actions-api-действия-с-заказами)
  - [📄 Лицензия](#-лицензия)

---

## 📌 О проекте
**Cafe Order Management System** — это веб-приложение для автоматизации заказов в кафе. Проект включает RESTful API и веб-интерфейс для работы с заказами, меню и отчетностью.

## 🚀 Версия
**Текущая версия:** `v0.2.0-PreAlpha`

## 🛠 Технологии
- **Язык программирования:** Python 3.8.10
- **Фреймворк:** Django 4.2.19 + Django REST Framework
- **Базы данных:** PostgreSQL, SQLite
- **Контейнеризация:** Docker, Docker Compose
- **Библиотеки:** django-filter, pytest
- **Frontend:** HTML/CSS (базовая стилизация)

---

## 🔧 Установка и запуск

### Клонирование репозитория
```sh
git clone https://github.com/AlexeyPol33/imei_telegram_bot.git
cd CafeOrderSystem
```

### Установка виртуального окружения
Рекомендуется использовать `pyenv` для управления версиями Python.

#### Установка Python
```sh
pyenv install 3.8.10
pyenv local 3.8.10  # В папке проекта
```

#### Создание и активация виртуального окружения
```sh
python -m venv venv
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate     # Для Windows
```

### Запуск в локальной среде

#### 1. Установка зависимостей
```sh
pip install -r requirements.txt
```

#### 2. Миграция базы данных
```sh
python manage.py migrate
```

#### 3. (Опционально) Загрузка тестовых данных меню
```sh
python manage.py load_meals --file=TestData/meals.yaml
```

#### 4. Запуск сервера
```sh
python manage.py runserver
```

---

### Развертывание с Docker
```sh
docker-compose up --build
```

---

## ✅ Текущий функционал
✅ RESTful API для взаимодействия с системой  
✅ Базовая навигация и стилизация веб-интерфейса  
✅ Корзина заказов  
✅ Добавление, удаление и поиск заказов  
✅ Управление статусами заказов  
✅ Расчет выручки за смену  
✅ Базовое тестирование  
✅ Базовая аутентификация
---

## 🔧 Запланированные функции
🔑 Разделение ролей пользователей (официант, администратор и т. д.)  
🔒 Изоляция внутреннего API  
🖼️ Поддержка загрузки изображений для меню  
🎯 Автоматизированное тестирование веб-интерфейса  
🌐 Улучшенный UI/UX  

---

## 📌 API Endpoints

### 📌 Основные
```http
[GET] / - Главная страница (временно дублирует `/menu/list/`)
[GET] /menu/list/ - Список доступных блюд
[GET] /menu/detail/{meal_id}/ - Детальная информация о блюде
[GET] /basket/ - Основная страница корзины
[GET] /management/ - Базовое меню управления заказами
[GET] /management/order/detail/{order_id}/ - Детализация заказа
[GET] /management/report/ - Генерация отчета за смену
[GET] /order/detail/{order_id}/ - Страница заказа
[GET] /order/list/one-line/ - Лист заказов для персонала
[GET] /order/list/ - Лист заказов для клиента (не реализован)
```

### 📦 Orders API (Работа с заказами и блюдами)
#### 📌 Meal Endpoints
```http
[GET]  /order-meal/meal/ - Получить список всех блюд
[POST] /order-meal/meal/ - Добавить новое блюдо
[GET]  /order-meal/meal/{meal_id}/ - Получить информацию о конкретном блюде
[PATCH] /order-meal/meal/{meal_id}/ - Частично обновить блюдо
[PUT]  /order-meal/meal/{meal_id}/ - Полностью обновить блюдо
[DELETE] /order-meal/meal/{meal_id}/ - Удалить блюдо
```

#### 📌 Order Endpoints
```http
[GET]  /order-meal/order/ - Получить список всех заказов
[POST] /order-meal/order/ - Создать новый заказ
[GET]  /order-meal/order/{order_id}/ - Получить детали заказа
[PATCH] /order-meal/order/{order_id}/ - Частично обновить заказ
[PUT]  /order-meal/order/{order_id}/ - Полностью обновить заказ
[DELETE] /order-meal/order/{order_id}/ - Удалить заказ
```

### 🛒 Basket API (Корзина)
```http
[GET] /basket/ - Основная страница корзины
[GET] /basket/add/{meal_id}/ - Добавить 1 шт. блюда в корзину
[GET] /basket/add/{meal_id}/{quantity}/ - Добавить несколько порций блюда
[GET] /basket/del/{meal_id}/ - Удалить 1 шт. блюда из корзины
[GET] /basket/del/{meal_id}/{quantity}/ - Удалить несколько порций блюда
```

### 💳 Order Actions API (Действия с заказами)
```http
[GET] /order/post/ - Оформить заказ
[GET] /order/detail/{order_id}/ - Получить информацию о заказе
[GET] /order/list/ - Список заказов
[GET] /order/list/one-line/ - Упрощенный список заказов для персонала
[GET] /order/button/pay/{order_id}/ - Оплатить заказ
[GET] /order/button/cancel/{order_id}/ - Отменить заказ
[DELETE] /order/delete/{order_id}/ - Удалить заказ
```
---

## 📄 Лицензия
Этот проект распространяется под лицензией **MIT**.

