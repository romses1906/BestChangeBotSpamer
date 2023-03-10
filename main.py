import asyncio
from aiogram import Dispatcher, Bot, types
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from requests_api import logic_func
from constants import TEMPL
import asyncpg
from config import POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT
from loader import bot, logger, dp
from sql import create_db

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s [%(asctime)s] %(message)s")


async def create_connect(bot: Bot) -> None:
    """
    Функция для создания подключения к БД и получения необходимых данных,
    отправка данных в соответствующие группы

    :param bot: Bot
    :return: None
    """
    # now = datetime(2022, 2, 23, 11, 37) # для тестов
    utcnow_time_str = str(datetime.utcnow().time()).split(':')
    utcnow_time_str[2] = '00'
    utcnow_time_str_res = ':'.join(utcnow_time_str)
    dateobj = datetime.strptime(utcnow_time_str_res, '%H:%M:%S')

    conn: asyncpg.Connection = await asyncpg.connect(user=POSTGRES_USER,
                                                     password=POSTGRES_PASSWORD,
                                                     host=POSTGRES_HOST,
                                                     port=POSTGRES_PORT)
    command_sql = "SELECT * FROM groups JOIN new_times ON new_times.group_id=groups.id WHERE new_times.time = $1;"
    rows = await conn.fetch(command_sql, dateobj)
    result_currencies = logic_func()
    for row in rows:
        row = dict(row)
        await bot.send_message(
            str(row['chat_id']),
            TEMPL.format(row['message'].replace('\\n', '\n'), result_currencies[0], result_currencies[1]),
            disable_web_page_preview=True
        )
    await conn.close()


async def set_default_commands(dp: Dispatcher) -> None:
    """
    Функция создания команд в меню бота

    :param dp: Dispatcher
    :return: None
    """
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
    ])


def set_scheduled_jobs(scheduler: AsyncIOScheduler, bot: Bot) -> None:
    """
    Функция создаия планировщика задач для бота

    :param scheduler: AsyncIOScheduler
    :param bot: Bot
    :return: None
    """
    scheduler.add_job(create_connect, 'cron', hour='3, 13', minute=30, start_date=datetime.utcnow(),
                      timezone='Europe/London', kwargs={'bot': bot})
    scheduler.add_job(create_connect, 'cron', hour='5, 8, 10', start_date=datetime.utcnow(),
                      timezone='Europe/London', kwargs={'bot': bot})


async def start_bot() -> None:
    """
    Функция запуска бота

    :return: None
    """
    scheduler = AsyncIOScheduler()

    # Ставим наши таски на запуск, передаем нужные переменные.
    set_scheduled_jobs(scheduler, bot)

    # start
    try:
        scheduler.start()
        await create_db()
        await dp.start_polling()
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start_bot())
