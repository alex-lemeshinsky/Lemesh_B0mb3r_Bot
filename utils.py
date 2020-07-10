from aiogram.dispatcher.filters.state import State, StatesGroup
from config import url
import requests

class Attack(StatesGroup):
    waiting_for_phone_number = State()
    waiting_for_number_of_cycles = State()

def start_attack(phone, number_of_cycles=1):
    r = requests.post(url, json = {"number_of_cycles": number_of_cycles, "phone": phone})
    if r.status_code == 200:
        id = r.json()['id']
        return "Атака началсь успешно! ID: " + id
    elif r.status_code == 500:
        return "Вы неправильно ввели номер телефона, попробуйте ещё раз."
    else:
        return "Произошла ошибка"