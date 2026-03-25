from core.config import MINUTES_TO_CHECK_CHANGES
import asyncio
from utils.api_client import ApiClient
from utils.helpers import get_changes
from utils.parser import parse_changes_url
from utils.changes_cache import ChangesCache
from utils.logger import Logger
from repositories.user_repository import UserRepository
from aiogram import Bot
from utils.formatters import get_changes_message

logger = Logger(__name__).get_logger()

async def get_changes_table_rows():
    main_page = await ApiClient.get_main_page()
    changes_url = parse_changes_url(main_page)

    changes_url_without_https_and_edit = changes_url[8:].split("/")[:-1]
    changes_url_without_https_and_edit.append("export?format=csv")
    download_url = "https://" + "/".join(changes_url_without_https_and_edit)

    csv_text = await ApiClient.get_file(download_url)
    table_rows = get_changes(csv_text)

    return table_rows

async def start_update_changes_cache_service(bot: Bot):
    changes_cache = ChangesCache()
    table_rows = await get_changes_table_rows()
    changes_cache.set(table_rows)
    while True:
        await asyncio.sleep(MINUTES_TO_CHECK_CHANGES*60)
        table_rows = await get_changes_table_rows()
        old_schedule = changes_cache.get()

        if table_rows != old_schedule:
            changes_cache.set(table_rows)

            users = await UserRepository.get_users()

            for user in users:
                grade = user.grade

                if not grade:
                    continue

                if grade not in table_rows:
                    continue

                if old_schedule.get(grade) == table_rows.get(grade):
                    continue

                text = "🔄 <b>Обновились замены!</b>\n\n"
                text += get_changes_message(table_rows, grade)

                try:
                    await bot.send_message(user.telegram_id, text)
                except Exception as e:
                    logger.warning(f"Не удалось отправить сообщение {user.telegram_id}: {e}")

            logger.info("Кэш замен обновлен, участники уведомлены")
        else:
            logger.info("Замены на сайте не изменились")