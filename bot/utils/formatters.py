from utils.helpers import get_current_lesson
from datetime import datetime, timedelta, timezone

emoji_prefixes = {"физическая": "🏀",
                  "алгебра": "🧮",
                  "вероятность": "📊",
                  "информатика": "💻",
                  "иностранный": "🌐",
                  "русский": "🇷🇺",
                  "биология": "🌱",
                  "разговор": "📢",
                  "география": "🌍",
                  "история": "🏛️",
                  "музыка": "🎵",
                  "труд(технология)": "📏",
                  "геометрия": "📐",
                  "изобразительное": "🎨",
                  "физика": "🚀",
                  "литература": "📚",
                  "химия": "🧪",
                  "россия-": "🧭"
                  }

def get_schedule_message(schedule: dict) -> str:
    text = '<b>🗓️ Расписание на неделю:</b>\n\n'

    for day, lessons in schedule.items():
        text += f'<b>📅 {day}</b>\n'

        for number, lesson in lessons.items():
            name = lesson.get("name")
            time = lesson.get("time")
            group = lesson.get("group")
            cab = lesson.get("cab")

            emoji_prefix = emoji_prefixes.get(name.lower().split()[0], "")

            if "groups" in lesson:
                text += f'{number}. {emoji_prefix} <b>{name}</b> — {time.replace(" ", "")}\n'

                if group:
                    text += f'   ├ группа {group} → каб. {cab}\n'

                for i, g in enumerate(lesson["groups"]):
                    prefix = "└" if len(lesson["groups"])-1-i == 0 else "├"
                    text += f'   {prefix} группа {g["group"]} → каб. {g["cab"]}\n'

            else:
                text += f'{number}. {emoji_prefix} <b>{name}</b> — {time.replace(" ", "")} | каб. {cab}\n'

        text += "\n"

    return text

def get_schedule_today_message(schedule: dict, day_of_week: str) -> str:
    text = f'<b>🗓️ Расписание на сегодня ({day_of_week}):</b>\n\n'

    for number, lesson in schedule.items():
        name = lesson.get("name")
        time = lesson.get("time")
        group = lesson.get("group")
        cab = lesson.get("cab")

        emoji_prefix = emoji_prefixes.get(name.lower().split()[0], "")

        if "groups" in lesson:
            text += f'{number}. {emoji_prefix} <b>{name}</b> — {time.replace(" ", "")}\n'

            if group:
                text += f'   ├ группа {group} → каб. {cab}\n'

            for i, g in enumerate(lesson["groups"]):
                prefix = "└" if len(lesson["groups"])-1-i == 0 else "├"
                text += f'   {prefix} группа {g["group"]} → каб. {g["cab"]}\n'

        else:
            text += f'{number}. {emoji_prefix} <b>{name}</b> — {time.replace(" ", "")} | каб. {cab}\n'

        text += "\n"

    return text

def get_schedule_tomorrow_message(schedule: dict, day_of_week: str) -> str:
    text = f'<b>🗓️ Расписание на завтра ({day_of_week}):</b>\n\n'

    for number, lesson in schedule.items():
        name = lesson.get("name")
        time = lesson.get("time")
        group = lesson.get("group")
        cab = lesson.get("cab")

        emoji_prefix = emoji_prefixes.get(name.lower().split()[0], "")

        if "groups" in lesson:
            text += f'{number}. {emoji_prefix} <b>{name}</b> — {time.replace(" ", "")}\n'

            if group:
                text += f'   ├ группа {group} → каб. {cab}\n'

            for i, g in enumerate(lesson["groups"]):
                prefix = "└" if len(lesson["groups"])-1-i == 0 else "├"
                text += f'   {prefix} группа {g["group"]} → каб. {g["cab"]}\n'

        else:
            text += f'{number}. {emoji_prefix} <b>{name}</b> — {time.replace(" ", "")} | каб. {cab}\n'

        text += "\n"

    return text

def get_lesson_message(number: int, lesson: dict) -> str:
    name = lesson.get("name")
    time = lesson.get("time")
    group = lesson.get("group")
    cab = lesson.get("cab")

    emoji_prefix = emoji_prefixes.get(name.lower().split()[0], "")

    if group in lesson:
        text = f"""<b>⏰ Текущий урок: {emoji_prefix} {name}:</b>
<b>🕜 Время:</b> {time}
<b>🔢 Урок по счету:</b> {number}

<b>Группы:</b>
"""

        if group:
            text += f'   ├ группа {group} → каб. {cab}\n'
        else:
            text += f'   ├ группа 1 → каб. {cab}\n'

        for i, g in enumerate(lesson["groups"]):
            prefix = "└" if len(lesson["groups"])-1-i == 0 else "├"
            text += f'   {prefix} группа {g["group"]} → каб. {g["cab"]}\n'
    
    else:
        text = f"""<b>⏰ Текущий урок: {emoji_prefix} {name}:</b>

<b>🕜 Время:</b> {time}
<b>🔢 Урок по счету:</b> {number}
<b>🚪 Кабиент:</b> {cab}
"""

    return text

def get_bell_message(time_to_bell: timedelta) -> str:
    try:
        minutes = int(time_to_bell.total_seconds()//60)
    except:
        minutes = time_to_bell.total_seconds()//60

    try:
        seconds = int(time_to_bell.total_seconds()%60)
    except:
        seconds = time_to_bell.total_seconds()%60


    return f"""🔔 Время до звонка: {minutes} минут {seconds} секунд"""
