import json
import requests
from typing import List
from bestchange_api import BestChange
import constants
from constants import DATA_DICT, BEST_USD, BEST_RUB
from loader import logger


def garantex(base_url: str) -> List:
    """
    Функция - отправляет запрос к API garantex.io и возвращает список со значениями.
    :param base_url: str
    :return: List
    """
    try:
        response = requests.get(base_url)
        try:
            results = response.json()
        except Exception:
            response = requests.get(base_url)
            results = response.json()
            return [round(float(results['asks'][0]['price']), 3), round(float(results['asks'][0]['factor']) * 100, 3)]
        return [round(float(results['asks'][0]['price']), 3), round(float(results['asks'][0]['factor']) * 100, 3)]
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def best_change(give_id: int, get_id: int) -> List:
    """
    Функция - отправляет запрос к API bestchange.ru и возвращает список со значениями.
    :param give_id: int
    :param get_id: int
    :return: List
    """
    try:
        api = BestChange()
        my = 840  # 954 - E-change
        result = api.rates().filter(give_id, get_id)
        place = 0
        first_place = None
        my_place = None
        if get_id == 91:
            variable = 'get'
        else:
            variable = 'give'
        for elem in result:
            if elem['city_id'] == 17:
                place += 1
                if place == 1:
                    first_place = [api.exchangers().get_by_id(elem['exchange_id']), round(elem[variable], 3), place]
                if elem['exchange_id'] == my:
                    #     my_place = ['<i><b>E-Change</b></i>', round(elem[variable], 3), place]
                    my_place = ['<i><b>YoChange</b></i>', round(elem[variable], 3), place]
                    break
        return [first_place, my_place]

    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def emoji_logic(place: int) -> str:
    """
    Логика распределения эмоджи
    :param place: int
    :return: str
    """
    try:
        if place == 1:
            my_emoji = '🏆'
        elif place <= 10:
            my_emoji = '🟢'
        elif place <= 20:
            my_emoji = '🟡'
        else:
            my_emoji = '🔴'
        return my_emoji
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def percentage_logic(cur: str, percent: float, place: int) -> List:
    """
    Функция - подгружает корректные емоджи в гарантекс
    :param place: int
    :param percent: float
    :param cur: str
    :return: List
    """
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            result = percent - data[cur]['percent']
            if cur == 'RUB':
                if (result * 100) >= 30:
                    rate = ['❤️']
                elif 11 <= (result * 100) <= 29:
                    rate = ['⬆️']
                elif -11 <= (result * 100) <= 11:
                    rate = ['⏸']
                elif -29 <= (result * 100) <= -11:
                    rate = ['⬇️']
                else:
                    rate = ['🆘']
            elif cur == 'USDT':
                if (result * 100) >= 30:
                    rate = ['🆘']
                elif 11 <= (result * 100) <= 29:
                    rate = ['⬆️']
                elif -11 <= (result * 100) <= 11:
                    rate = ['⏸']
                elif -29 <= (result * 100) <= -11:
                    rate = ['⬇️']
                else:
                    rate = ['❤️']
            else:
                if result >= 0.3:
                    rate = ['❤️']
                elif 0.1 <= result <= 0.29:
                    rate = ['⬆️']
                elif -0.1 <= result <= 0.1:
                    rate = ['⏸']
                elif -0.29 <= result <= -0.1:
                    rate = ['⬇️']
                else:
                    rate = ['🆘']
            if data[cur]['place'] > place:
                rate.append('⬆️')
            elif data[cur]['place'] == place:
                rate.append('⏸')
            else:
                rate.append('⬇️')
        DATA_DICT[cur]['percent'] = percent
        DATA_DICT[cur]['place'] = place
        return rate
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def spred_logic(spred: float) -> str:
    """
    Функция - обрабатывает спред

    :param spred: float
    :return: str
    """
    try:
        if spred < 0:
            spred = f'({spred}%) ⁉️'
        elif spred < 1.0:
            spred = f'({spred}%) 🌶️'
        elif spred < 2.0:
            spred = f'({spred}%) 🍋'
        elif spred < 3.0:
            spred = f'({spred}%) 🍆'
        else:
            spred = f'({spred}%) 😱'
        return spred
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def logic_func() -> tuple:
    """
    Функция парсинга информации с сайтов

    :return: Tuple
    """

    gar_rub = garantex(constants.GAR_RUB)
    best_rub = best_change(10, 91)
    first_rub = round((best_rub[0][1] / (gar_rub[0] / (gar_rub[1] / 100 + 1)) - 1) * 100, 2)
    my_rub = round((best_rub[1][1] / (gar_rub[0] / (gar_rub[1] / 100 + 1)) - 1) * 100, 2)
    rub_emoji = emoji_logic(best_rub[1][2])
    rub_rate = percentage_logic('RUB', gar_rub[0], best_rub[1][2])
    spred = round(gar_rub[1] - first_rub, 2)
    spred = spred_logic(spred)
    my_spred = round(gar_rub[1] - my_rub, 2)
    my_spred = spred_logic(my_spred)
    rub_template = constants.TEMPLATE.format(
        'https://garantex.io/trading/usdtrub', 'RUB', 'RUB', gar_rub[0], gar_rub[1], rub_rate[0],
        best_rub[0][2], best_rub[0][0], 1, best_rub[0][1], first_rub, spred, rub_emoji, rub_rate[1],
        best_rub[1][2], f"<a href='{BEST_RUB}'>{best_rub[1][0]}</a>", 1, best_rub[1][1], my_rub, my_spred
    )
    gar_usd = garantex(constants.GAR_USD)
    best_usd = best_change(10, 89)
    first_usd = round((best_usd[0][1] - 1) * 100, 2)
    my_usd = round((best_usd[1][1] - 1) * 100, 2)
    usd_emoji = emoji_logic(best_usd[1][2])
    if best_usd[1][1] <= 1.0:
        my_usd *= 1
    else:
        my_usd *= -1
    if best_usd[0][1] <= 1.0:
        first_usd *= 1
    else:
        first_usd *= -1
    usd_rate = percentage_logic('USD', gar_usd[1], best_usd[1][2])
    spred = round(gar_usd[1] - first_usd, 2)
    spred = spred_logic(spred)
    my_spred = round(gar_usd[1] - my_usd, 2)
    my_spred = spred_logic(my_spred)
    usd_template = constants.TEMPLATE.format(
        'https://garantex.io/trading/usdtusd', 'USD', 'USD', gar_usd[0], gar_usd[1], usd_rate[0],
        best_usd[0][2], best_usd[0][0], best_usd[0][1], 1, first_usd, spred, usd_emoji, usd_rate[1],
        best_usd[1][2], f"<a href='{BEST_USD}'>{best_usd[1][0]}</a>", best_usd[1][1], 1, my_usd, my_spred
    )
    with open('data.json', 'w') as file:
        json.dump(DATA_DICT, file, indent=4)

    return rub_template, usd_template
