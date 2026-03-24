from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from messages.common import start_message
from utils.api_client import ApiClient
from utils.logger import Logger
from utils.schedule_cache import ScheduleCache

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

command_router = Router()
logger = Logger(__name__).get_logger()

@command_router.message(CommandStart())
async def start(message: types.Message):
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /start")
    await message.answer(start_message)

@command_router.message(Command("schedule"))
async def schedule(message: types.Message):
    grade = message.text.split()[1]
    logger.info(f"Пользователь @{message.from_user.username} вызвал команду /schedule для класса {grade}")

    cache = ScheduleCache()
    if cache.get(grade) is None:
        rasp = await ApiClient.get_grade_schedule(grade)
        cache.set(grade, rasp)
        logger.info(f"Расписание для класса {grade} получено с сайта")
    else:
        rasp = cache.get(grade)
        logger.info(f"Расписание для класса {grade} получено из кэша")

    text = '<b>🗓️ Расписание на неделю:</b>\n\n'

    for day, lessons in rasp.items():
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

    await message.answer(text)