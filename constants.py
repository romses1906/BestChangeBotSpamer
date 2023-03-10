"""
Файл - для общей замены сообщений в боте
"""

BEST_RUB = 'https://www.bestchange.ru/tether-trc20-to-cash-ruble-in-nsk.html'
BEST_USD = 'https://www.bestchange.ru/tether-trc20-to-dollar-cash-in-nsk.html'
GAR_RUB = 'https://garantex.io/api/v2/depth?market=usdtrub'
GAR_USD = 'https://garantex.io/api/v2/depth?market=usdtusd'


TEMPLATE = '<a href="{}"><b>USDT - {} #покупка</b></a>\n' \
           '<i>Tether TRC20 (USDT) на</i> Наличные {}' \
           '\n<i>Garantex</i>\n' \
           'Продажа: 1 => {} ({}%){}\n\n' \
           '🏆{}st. {} {} => {} ({}%) спред {}\n' \
           '...\n' \
           '{}{}{}st. {} {} => {} ({}%) спред {}'

TEMPL = "{}\n___________________________\n{}\n___________________________\n{}"


DATA_DICT = {
    "RUB": {
        'percent': 0,
        'place': 0
    },
    "USD": {
        'percent': 0,
        'place': 0
    },
    "USDT": {
        'percent': 0,
        'place': 0
    },
}

