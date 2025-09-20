# Telegram Admin Bot with Tkinter GUI

![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)
![Aiogram](https://img.shields.io/badge/aiogram-3.19-green)
![SQLite](https://img.shields.io/badge/database-sqlite-lightgrey)

## Описание проекта

Этот проект представляет собой **Telegram-бота для приёма заявок от пользователей** с интеграцией **Tkinter GUI для администратора**.  
Администратор может видеть новые заявки в реальном времени и отвечать на них прямо из GUI. Ответ автоматически отправляется пользователю в Telegram.  

Основные особенности:

- Пользователи могут отправлять заявки через Telegram.
- Заявки сохраняются в **SQLite базу данных**.
- Tkinter GUI показывает список заявок в **реальном времени**.
- Администратор может писать ответы и отправлять их пользователю прямо из GUI.
- Авто-обновление списка заявок каждые 2 секунды.
- Поддержка нескольких администраторов и пользователей.

---

## Установка

1. Клонируйте репозиторий:
  ```bash
  git clone https://github.com/RiderMC126/TkBotRequests.git
  cd TkBotRequests
  ```
2. Создайте виртуальное окружение и установите зависимости:
  ```bash
  python -m venv venv
  source venv/bin/activate   # Linux/macOS
  venv\Scripts\activate      # Windows

  pip install --upgrade pip
  pip install aiogram
  ```
3. Создайте файл bot/config.py и добавьте ваш токен бота:
   ```bash
   TOKEN = "ВАШ_TELEGRAM_BOT_TOKEN"
   ```

---

## Использование
```bash
python main.py
```



   


