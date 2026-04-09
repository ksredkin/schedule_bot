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

Schedule Bot — это Telegram-бот для удобного просмотра школьного расписания ВМЛ.

Бот позволяет быстро получить актуальную информацию о занятиях и изменениях без необходимости заходить на сайт школы.

⚠️ Бот является неофициальным

## 📊 Статистика

🚀 Ботом уже пользуется 20+ человек

📈 Проект находится в активной разработке и продолжает расти

## 🎯 Возможности
- 📅 Просмотр расписания на сегодня
- 🗓 Просмотр расписания на неделю
- 📆 Просмотр расписания на завтра
- 📍 Определение кабинета текущего урока
- ⏳ Подсчёт времени до следующего звонка
- 🔔 Уведомления о заменах
- ⚙️ Установка класса по умолчанию
- ⚡ Кэширование расписания для ускорения работы

## 🧠 Как работает
1. Бот отправляет POST-запрос к сайту школы
2. Получает HTML-страницу с расписанием
3. Парсит её с помощью BeautifulSoup
4. Преобразует в структурированные данные
5. Кэширует результат
6. Отправляет пользователю

## 🚀 Запуск проекта
### 1. Клонирование
```bash
git clone https://github.com/ksredkin/schedule-bot.git
cd schedule-bot
```

### 2. Настройка окружения
```bash
cp .env.example .env
nano .env
```

### 3. Запуск через Docker
```bash
docker-compose up --build
```

## 📌 Пример ответа бота

```
🗓️ Расписание на сегодня (среда):

1. 📊 Вероятность и статистика — 08:00-08:40 | каб. 226

2. 🚀 Физика — 08:50-09:30 | каб. 122

3. 🧮 Алгебра — 09:40-10:20 | каб. 226

4. 🌍 География — 10:40-11:20 | каб. 125

5. 🇷🇺 Русский язык — 11:30-12:10 | каб. 133

6. 📚 Литература — 12:20-13:00 | каб. 133

7. 🏛️ История — 13:10-13:50 | каб. 223
```

---

## ⭐ Примечание

Проект сделан в учебных целях и для личного использования.

Если проект оказался полезным — можно поставить ⭐ на GitHub! 🚀