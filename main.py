from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token='5411588162:AAGHrl2GOjG6Uz1F2DxlTmrs6PQ_Z4JAIuM')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Hello")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

executor.start_polling(dp)
