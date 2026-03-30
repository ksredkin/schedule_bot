from datetime import timedelta

emoji_prefixes = {
    "физическая": "🏀",
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
    "россия-": "🧭",
}


def get_schedule_message(schedule: dict) -> str:
    text = "<b>🗓️ Расписание на неделю:</b>\n\n"

    for day, lessons in schedule.items():
        text += f"<b>📅 {day}</b>\n"

        if not lessons:
            text += "\nУроков нет\n\n"
            continue

        for number, lesson in lessons.items():
            name = lesson.get("name")
            time = lesson.get("time")
            group = lesson.get("group")
            cab = lesson.get("cab")

            emoji_prefix = emoji_prefixes.get(name.lower().split()[0], "")

            if "groups" in lesson:
                text += f"{number}. {emoji_prefix} <b>{name}</b> — {time.replace(' ', '')}\n"

                if group:
                    text += f"   ├ группа {group} → каб. {cab}\n"

                for i, g in enumerate(lesson["groups"]):
                    prefix = "└" if len(lesson["groups"]) - 1 - i == 0 else "├"
                    text += f"   {prefix} группа {g['group']} → каб. {g['cab']}\n"

            else:
                text += f"{number}. {emoji_prefix} <b>{name}</b> — {time.replace(' ', '')} | каб. {cab}\n"

        text += "\n"

    return text


def get_schedule_today_message(schedule: dict, day_of_week: str) -> str:
    text = f"<b>🗓️ Расписание на сегодня ({day_of_week.lower()}):</b>\n\n"

    if not schedule:
        text += "Уроков нет"
        return text

    for number, lesson in schedule.items():
        name = lesson.get("name")
        time = lesson.get("time")
        group = lesson.get("group")
        cab = lesson.get("cab")

        emoji_prefix = emoji_prefixes.get(name.lower().split()[0], "")

        if "groups" in lesson:
            text += (
                f"{number}. {emoji_prefix} <b>{name}</b> — {time.replace(' ', '')}\n"
            )

            if group:
                text += f"   ├ группа {group} → каб. {cab}\n"

            for i, g in enumerate(lesson["groups"]):
                prefix = "└" if len(lesson["groups"]) - 1 - i == 0 else "├"
                text += f"   {prefix} группа {g['group']} → каб. {g['cab']}\n"

        else:
            text += f"{number}. {emoji_prefix} <b>{name}</b> — {time.replace(' ', '')} | каб. {cab}\n"

        text += "\n"

    return text


def get_schedule_tomorrow_message(schedule: dict, day_of_week: str) -> str:
    text = f"<b>🗓️ Расписание на завтра ({day_of_week}):</b>\n\n"

    if not schedule:
        text += "Уроков нет"
        return text

    for number, lesson in schedule.items():
        name = lesson.get("name")
        time = lesson.get("time")
        group = lesson.get("group")
        cab = lesson.get("cab")

        emoji_prefix = emoji_prefixes.get(name.lower().split()[0], "")

        if "groups" in lesson:
            text += (
                f"{number}. {emoji_prefix} <b>{name}</b> — {time.replace(' ', '')}\n"
            )

            if group:
                text += f"   ├ группа {group} → каб. {cab}\n"

            for i, g in enumerate(lesson["groups"]):
                prefix = "└" if len(lesson["groups"]) - 1 - i == 0 else "├"
                text += f"   {prefix} группа {g['group']} → каб. {g['cab']}\n"

        else:
            text += f"{number}. {emoji_prefix} <b>{name}</b> — {time.replace(' ', '')} | каб. {cab}\n"

        text += "\n"

    return text


def get_lesson_message(number: int, lesson: dict) -> str:
    name = lesson.get("name")
    time = lesson.get("time")
    group = lesson.get("group")
    cab = lesson.get("cab")

    emoji_prefix = emoji_prefixes.get(name.lower().split()[0], "")

    if group:
        text = f"""<b>⏰ Текущий урок: {emoji_prefix} {name}</b>
<b>🕜 Время:</b> {time}
<b>🔢 Урок по счету:</b> {number}

<b>Группы:</b>
"""

        if group:
            text += f"   ├ группа {group} → каб. {cab}\n"
        else:
            text += f"   ├ группа 1 → каб. {cab}\n"

        for i, g in enumerate(lesson["groups"]):
            prefix = "└" if len(lesson["groups"]) - 1 - i == 0 else "├"
            text += f"   {prefix} группа {g['group']} → каб. {g['cab']}\n"

    else:
        text = f"""<b>⏰ Текущий урок: {emoji_prefix} {name}</b>

<b>🕜 Время:</b> {time}
<b>🔢 Урок по счету:</b> {number}
<b>🚪 Кабиент:</b> {cab}
"""

    return text


def get_next_lesson_message(next_time_to_bell: timedelta, next_lesson: dict) -> str:
    name = next_lesson.get("name")
    time = next_lesson.get("time")
    group = next_lesson.get("group")
    cab = next_lesson.get("cab")

    emoji_prefix = emoji_prefixes.get(name.lower().split()[0], "")

    try:
        minutes = int(next_time_to_bell.total_seconds() // 60)
    except Exception:
        minutes = next_time_to_bell.total_seconds() // 60

    try:
        seconds = int(next_time_to_bell.total_seconds() % 60)
    except Exception:
        seconds = next_time_to_bell.total_seconds() % 60

    if group:
        text = f"""<b>⏰ Следующий урок: {emoji_prefix} {name}</b>
<b>⏳ До звонка:</b> {minutes} минут {seconds} секунд
<b>🕜 Время:</b> {time}

<b>Группы:</b>
"""

        text += f"   ├ группа 1 → каб. {cab}\n"

        for i, g in enumerate(next_lesson["groups"]):
            prefix = "└" if len(next_lesson["groups"]) - 1 - i == 0 else "├"
            text += f"   {prefix} группа {g['group']} → каб. {g['cab']}\n"

    else:
        text = f"""<b>⏰ Следующий урок: {emoji_prefix} {name}</b>

<b>⏳ До звонка:</b> {minutes} минут {seconds} секунд
<b>🕜 Время:</b> {time}
<b>🚪 Кабиент:</b> {cab}
"""

    return text


def get_bell_message(time_to_bell: timedelta) -> str:
    try:
        minutes = int(time_to_bell.total_seconds() // 60)
    except Exception:
        minutes = time_to_bell.total_seconds() // 60

    try:
        seconds = int(time_to_bell.total_seconds() % 60)
    except Exception:
        seconds = time_to_bell.total_seconds() % 60

    return f"""🔔 Время до звонка: {minutes} минут {seconds} секунд"""


def get_changes_message(rows: list, _grade: str) -> str:
    text = "<b>🔄 Замены уроков:</b>\n\n"

    cleaned_rows = []

    for row in rows:
        if len(row) < 6:
            continue

        if all(not cell.strip() for cell in row):
            continue

        if row[0].lower() == "урок":
            continue

        lesson, grade, _, _, _, _ = row

        if not grade or not lesson:
            continue

        cleaned_rows.append(row)

    replaces = {}

    for row in cleaned_rows:
        lesson, grade, subject, teacher, new_subject, cab = row

        if grade not in replaces:
            replaces[grade] = []

        replaces[grade].append([lesson, subject, teacher, new_subject, cab])

    current_grade_replaces = replaces.get(_grade.lower())

    if not current_grade_replaces:
        text += "Замен не найдено."
        return text

    for replace in current_grade_replaces:
        lesson, subject, teacher, new_subject, cab = replace

        text += f"{lesson} урок: {subject}"

        if new_subject:
            text += f" → {new_subject}"

        if teacher and teacher != "нет":
            text += f" ({teacher})"

        if cab:
            text += f" | каб. {cab}"

        text += "\n\n"

    return text
