import asyncio
import asyncpg
import logging
from config import POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT
from loader import logger

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s [%(asctime)s] %(message)s")


async def create_db() -> None:
    """
    Функция для создания БД

    :return: None
    """
    create_db_command = open("create_db.sql", "r").read()
    logging.info("Connecting to database...")
    conn: asyncpg.Connection = await asyncpg.connect(user=POSTGRES_USER,
                                                     password=POSTGRES_PASSWORD,
                                                     host=POSTGRES_HOST,
                                                     port=POSTGRES_PORT)
    try:
        await conn.execute(create_db_command)
    except asyncpg.exceptions.DuplicateTableError as error:
        logger.error('В работе бота возникло исключение', exc_info=error)
    await conn.close()
    logging.info("Database created")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
