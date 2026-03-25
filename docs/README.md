# 📅 Schedule Bot (ВМЛ)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-2CA5E0?style=for-the-badge\&logo=telegram\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge\&logo=postgresql\&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge\&logo=sqlalchemy\&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-00A98F?style=for-the-badge\&logo=alembic\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4CAF50?style=for-the-badge)
![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge\&logo=poetry\&logoColor=white)

---

## 📌 Описание

**Schedule Bot** — это Telegram-бот для удобного просмотра школьного расписания ВМЛ.

Бот позволяет быстро получить:

* расписание на сегодня
* расписание на неделю
* кабинет текущего урока
* время до звонка
* информацию о заменах

⚠️ **Бот является неофициальным**

---

## 🎯 Возможности

* 📅 Просмотр расписания на сегодня
* 🗓 Просмотр расписания на неделю
* 📍 Определение кабинета текущего урока
* ⏳ Подсчёт времени до звонка
* 🔔 Уведомления о заменах (в разработке)
* ⚙️ Установка класса по умолчанию
* ⚡ Кэширование расписания

---

## 🤖 Команды бота

```
/start
/schedule
/schedule {class}
/schedule_today
/schedule_today {class}
/schedule_tomorrow
/schedule_tomorrow {class}
/set_my_class
```

### 📖 Описание команд

* `/schedule` — расписание на неделю для класса, выбранного по умолчанию
* `/schedule {class}` — расписание конкретного класса (например: `7д`)
* `/schedule_today` — расписание на сегодня для класса, выбранного по умолчанию
* `/schedule_today {class}` — расписание на сегодня конкретного класса (например: `7д`)
* `/schedule_today` — расписание на завтра  для класса, выбранного по умолчанию
* `/schedule_today {class}` — расписание на завтра конкретного класса (например: `7д`)
* `/set_my_class` — установить класс по умолчанию

---

## 🧠 Как работает

1. Бот отправляет POST-запрос к сайту школы
2. Получает HTML-страницу с расписанием
3. Парсит её с помощью BeautifulSoup
4. Преобразует в структурированные данные
5. Кэширует результат
6. Отправляет пользователю

---


## 🚀 Запуск проекта

### 1. Клонирование

```bash
git clone https://github.com/ksredkin/schedule-bot.git
cd schedule-bot
```

---

### 2. Настройка окружения

```bash
cp .env.example .env
nano .env
```

Заполни переменные:

```
BOT_TOKEN=
PROXY=

DB_USER=
DB_PASSWORD=
DB_PORT=
DB_NAME=
```

---

### 3. Запуск через Docker

```bash
docker-compose up --build
```

---

## 📌 Пример ответа бота

```
📅 Понедельник
1. 📢 Разговор о важном — 08:00-08:40 | каб. 137
2. 🌱 Биология — 08:50-09:30 | каб. 126
```

---

## ⭐ Примечание

Проект сделан в учебных целях и для личного использования.

Если проект оказался полезным - можно поставить ⭐ на GitHub!