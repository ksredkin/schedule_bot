from core.config import MINUTES_TO_CHECK_CHANGES
import asyncio
from utils.api_client import ApiClient
from utils.helpers import get_changes
from utils.parser import parse_changes_url
from utils.changes_cache import ChangesCache
from utils.logger import Logger

logger = Logger(__name__).get_logger()

async def start_update_changes_cache_service():
    changes_cache = ChangesCache()
    while True:
        asyncio.sleep(MINUTES_TO_CHECK_CHANGES*60)

        main_page = await ApiClient.get_main_page()
        changes_url = parse_changes_url(main_page)

        changes_url_without_https_and_edit = changes_url[8:].split("/")[:-1]
        changes_url_without_https_and_edit.append("export?format=csv")
        download_url = "https://" + "/".join(changes_url_without_https_and_edit)

        csv_text = await ApiClient.get_file(download_url)
        table_rows = get_changes(csv_text)

        if table_rows != changes_cache.get():
            changes_cache.set(table_rows)
            logger.info("Кэш замен обновлен")
        else:
            logger.info("Замены на сайте не изменились")