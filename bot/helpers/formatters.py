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