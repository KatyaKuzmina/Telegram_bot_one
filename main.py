from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token='5411588162:AAGHrl2GOjG6Uz1F2DxlTmrs6PQ_Z4JAIuM')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Hello")

@dp.message_handler(commands=['help'])
async def welcome(message: types.Message):
    await message.answer("Some information")

answers = []

lang1 = KeyboardButton('English 👍')
lang2 = KeyboardButton('russian 💪')
lang3 = KeyboardButton('Other language 🤝')
lang_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(lang1).add(lang2).add(lang3)

@dp.message_handler(commands=['language'])
async def welcome(message: types.Message):
    await message.answer('Choose lang', reply_markup=lang_kb)

en_options1 = KeyboardButton('Psychological support 🧠')
en_options2 = KeyboardButton('Supplies: food, medicine, hormones, ... 🍇')
en_options3 = KeyboardButton('Border crossing 🏇')
en_options4 = KeyboardButton('Other help 📚')
en_options_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(en_options1).add(en_options2).add(en_options3).add(en_options4)

#### selecting what you need
@dp.message_handler(regexp='English 👍')
async def english(message: types.Message):
    answers.append(message.text)
    await message.answer('What do you need?', reply_markup = en_options_kb)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

"""""
@dp.message_handler(commands=['button'])
async def button()
"""""

"""""
Language change
"""""

executor.start_polling(dp)
