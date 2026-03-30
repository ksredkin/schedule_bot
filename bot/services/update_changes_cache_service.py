import asyncio

from aiogram import Bot

from core.config import MINUTES_TO_CHECK_CHANGES
from repositories.user_repository import UserRepository
from utils.api_client import ApiClient
from utils.changes_cache import ChangesCache
from utils.formatters import get_changes_message
from utils.helpers import get_changes
from utils.logger import Logger
from utils.parser import parse_changes_url

logger = Logger(__name__).get_logger()


async def get_changes_table_rows() -> list[list[str]] | None:
    try:
        main_page = await ApiClient.get_main_page()

        if not main_page:
            logger.warning(
                "Не удалось получить главную страницу для извлечения ссылки на замены"
            )
            return None

        changes_url = parse_changes_url(main_page)

        if not changes_url:
            logger.warning(
                "Не удалось найти ссылку на страницу с заменами на главной странице"
            )
            return None

        changes_url_without_https_and_edit = changes_url[8:].split("/")[:-1]
        changes_url_without_https_and_edit.append("export?format=csv")
        download_url = "https://" + "/".join(changes_url_without_https_and_edit)

        csv_text = await ApiClient.get_file(download_url)

        if not csv_text:
            logger.warning("Полученный CSV с изменениями пустой")
            return None

        table_rows = get_changes(csv_text)

        return table_rows
    except Exception as e:
        logger.critical(f"Не удалось получить строки таблицы изменений: {e}")
        return None


def parse_changes_table_rows(
    table_rows: list[list[str]],
) -> dict[str, list[dict[str, str | None]]]:
    changes_by_grade: dict[str, list[dict[str, str | None]]] = {}

    for row in table_rows[1:]:
        if len(row) < 5:
            continue

        grade = row[0].strip().upper()
        time = row[1].strip()
        subject = row[2].strip()
        teacher = row[3].strip()
        room = row[4].strip()

        change_info: dict[str, str | None] = {
            "time": time,
            "subject": subject,
            "teacher": teacher,
            "room": room,
        }

        if grade not in changes_by_grade:
            changes_by_grade[grade] = []

        changes_by_grade[grade].append(change_info)

    return changes_by_grade


async def start_update_changes_cache_service(bot: Bot) -> None:
    changes_cache = ChangesCache()
    while True:
        table_rows = await get_changes_table_rows()
        old_schedule = changes_cache.get()

        if not table_rows:
            logger.warning(
                "Не удалось получить новые данные о заменах, пропуск проверки изменений"
            )
            continue

        if table_rows != old_schedule:
            changes_cache.set(table_rows)

            users = await UserRepository.get_users()

            if not users:
                logger.info(
                    "Нет зарегистрированных пользователей для уведомления об изменениях"
                )
                continue

            for user in users:
                grade = user.grade

                if not grade:
                    continue

                if grade not in table_rows:
                    continue

                if not old_schedule:
                    continue

                if parse_changes_table_rows(old_schedule).get(
                    str(grade)
                ) == parse_changes_table_rows(table_rows).get(str(grade)):
                    continue

                if not table_rows:
                    continue

                text = "🔄 <b>Обновились замены!</b>\n\n"

                text += get_changes_message(table_rows, str(grade))

                try:
                    user_telegram_id: int = int(user.telegram_id)
                    await bot.send_message(user_telegram_id, text)
                except Exception as e:
                    logger.warning(
                        f"Не удалось отправить сообщение {user.telegram_id}: {e}"
                    )

            logger.info("Кэш замен обновлен, участники уведомлены")
        else:
            logger.info("Замены на сайте не изменились")

        await asyncio.sleep(MINUTES_TO_CHECK_CHANGES * 60)
