# 📨 Telegram Admin Bot with Tkinter GUI

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Aiogram](https://img.shields.io/badge/Aiogram-3.19-green?logo=telegram)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-orange)

> Управление заявками пользователей через Telegram с мгновенным контролем и ответами из красивого GUI на Tkinter.

---

## 🚀 Описание проекта

Этот проект представляет собой **Telegram-бота для приёма заявок** с **Tkinter GUI для администратора**.  
Администратор может видеть новые заявки в реальном времени, отвечать на них и отслеживать статус заявок без перезапуска приложения.  

### Особенности:

- Пользователи отправляют заявки через Telegram.
- Заявки автоматически сохраняются в **SQLite**.
- Tkinter GUI показывает заявки в **реальном времени**.
- Авто-обновление списка каждые 3 секунды.
- Отправка ответов через GUI напрямую пользователю.
- Лёгкий и красивый интерфейс для администратора.
- Поддержка нескольких пользователей и администраторов.

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



   


