import csv
from io import StringIO

from src.bot.utils.logger import Logger

logger = Logger(__name__).get_logger()


def get_changes(csv_text: str) -> list[list[str]] | None:
    if not isinstance(csv_text, str):
        return None

    try:
        reader = csv.reader(StringIO(csv_text))
        rows = list(reader)
        return rows
    except Exception as e:
        logger.critical(f"Не удалось спарсить csv файл замен: {e}")
        return None
