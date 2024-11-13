import locale
from datetime import datetime

import pytest

from handlers.schedule import select_group


def test_day():
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    today = datetime.now().strftime("%A").capitalize()
    print(today)